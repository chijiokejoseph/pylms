from pathlib import Path

from ..cli import input_bool, input_email, input_option, input_path, input_str
from ..cli_utils import emphasis, verify_gmail
from ..constants import COURSES, DATA_PATH
from ..errors import ForcedExitError, Result, eprint
from ..info import print_info, printpass
from .config import Config
from .facilitator import Facilitator


def input_dir() -> Result[Path]:
    """Prompt for and validate the project's data directory.

    Returns:
        Result[str]: Data directory path on success or error Result.
    """
    while True:
        result: Result[Path] = input_path(
            "Enter the location to save files to. Enter the letter 's' to skip. [Ensure that the location has no file called 'data']: "
        )
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            eprint(f"{err}")
            continue
        data_dir = result.unwrap()

        if data_dir.name.lower() == "s":
            print("Skipping Data Path setup")
            print(f"Data Path not set. Defaulting to {DATA_PATH}")
            return Result.ok(DATA_PATH)

        if not data_dir.is_dir():
            eprint("The save path entered is not a directory")
            continue

        sub_dirs = [Path(item) for item in data_dir.iterdir()]
        sub_data_dirs = [
            item for item in sub_dirs if item.is_dir() and item.name == "data"
        ]

        if len(sub_data_dirs) > 0:
            eprint("The save path entered contains a directory called 'data'")
            continue

        if not data_dir.exists():
            eprint("The save path entered does not exist")
            continue

        data_dir = data_dir / "data"
        printpass(f"Data Path has been successfully initialized to {emphasis(str(data_dir))}")
        return Result.ok(data_dir)


def input_course_name() -> Result[str]:
    """Prompt the user to select a course name.

    Returns:
        Result[str]: Course name on success or error Result.
    """
    while True:
        result = input_option(COURSES, prompt="Select the course name")
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            eprint(f"{err}")
            continue

        _, course_name = result.unwrap()
        printpass(f"You have selected {course_name}\n")
        return Result.ok(course_name)


def input_facilitators() -> Result[list[Facilitator]]:
    """Prompt for facilitator names and emails.

    Returns:
        Result[list[Facilitator]]: List of facilitators on success or error Result.
    """
    facilitators: list[Facilitator] = []

    while True:
        result = input_str(
            "Enter facilitator name: ",
            test_fn=lambda x: len(x.strip()) > 0,
            diagnosis="Name cannot be empty",
            lower_case=False,
        )
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            eprint(f"{err}")
            continue
        name = result.unwrap()

        result = input_str(
            "Enter facilitator Gmail: ",
            test_fn=verify_gmail,
            diagnosis="Invalid Gmail address",
            lower_case=False,
        )
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            eprint(f"{err}")
            continue
        gmail = result.unwrap()

        facilitator = Facilitator.build(name=name, gmail=gmail)
        if facilitator.is_err():
            err = facilitator.unwrap_err()
            if isinstance(err, ForcedExitError):
                return facilitator.propagate()
            eprint(f"{err}")
            continue

        facilitators.append(facilitator.unwrap())
        printpass(f"Added facilitator: {name} ({gmail})")

        result = input_bool("Add another facilitator?")
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            eprint(f"{err}")
            continue
        if not result.unwrap():
            break

    return Result.ok(facilitators)


def input_admin() -> Result[tuple[str, str]]:
    msg = """You have successfully added all facilitators.
Please enter an admin gmail and password to a gmail app 
with less secure access enabled.
This admin gmail will be used for the following:
    - Sending emails to students
    - Storing student emails
"""

    print_info(msg)

    while True:
        result = input_email(msg="Enter admin gmail: ", gmail=True)
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            result.print_if_err()
            continue

        admin = result.unwrap()

        password = input_str("Enter admin app password: ", lower_case=False)
        if password.is_err() and isinstance(password.error, ForcedExitError):
            return password.propagate()
        elif password.is_err():
            password.print_if_err()
            continue

        password = password.unwrap()

        return Result.ok((admin, password))


def setup_new_config() -> Result[Config]:
    """Setup new config by prompting for all required fields.

    Returns:
        Result[Config]: Newly created Config instance on success or error Result.
    """
    result = input_dir()
    if result.is_err():
        return result.propagate()
    data_dir = result.unwrap()

    result = input_course_name()
    if result.is_err():
        return result.propagate()
    course_name = result.unwrap()

    result = input_facilitators()
    if result.is_err():
        return result.propagate()
    facilitators = result.unwrap()

    result = input_admin()
    if result.is_err():
        return result.propagate()
    admin, password = result.unwrap()

    config = Config()
    config.data_dir = str(data_dir)
    config.course_name = course_name
    config.facilitators = facilitators
    config.admin = admin
    config.set_password(password)

    DATA_PATH.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    return Result.ok(config)

from pathlib import Path
from pylms.errors import LMSError, Result, Unit
from pylms.config.config import Config
from pylms.constants import DEFAULT_DATA_PATH
from pylms.constants import COURSES


def input_fn(msg: str) -> Result[str]:
    msg += "\n[To forcefully exit the operation enter 'quit', 'exit' or 'q']: "
    user_input: str = input(msg)
    if user_input in ["quit", "exit", "q"]:
        return Result[str].err(LMSError("You quit the operation"))
    else:
        return Result[str].ok(user_input)


def input_dir(table: Config) -> Result[Unit]:
    from pylms.cli import input_str

    save_path = Path(table.settings.data_dir)
    if save_path.exists() and save_path != Path(""):
        print(f"Data Path has been successfully initialized to {save_path}")
        return Result[Unit].unit()
    result: Result[str] = input_str(
        "Enter the location to save files to. Enter the letter 's' to skip. [Ensure that the location has no file called 'data']: "
    )
    if result.is_err():
        return Result[Unit].err(result.unwrap_err())
    data_dir: str = result.unwrap().strip()
    if data_dir.lower() == "s":
        print("Skipping Data Path setup")
        print(f"Data Path not set. Defaulting to {DEFAULT_DATA_PATH}")
        table.settings.data_dir = str(DEFAULT_DATA_PATH)
        return Result[Unit].unit()

    data_path: Path = Path(data_dir).resolve()
    if not data_path.is_dir():
        return Result[Unit].err(LMSError("The save path entered is not a directory"))
    for each_item in data_path.iterdir():
        each_path: Path = Path(each_item)
        if each_path.is_dir() and each_path.name == "data":
            return Result[Unit].err(
                LMSError("The save path entered contains a directory called 'data'")
            )

    if not data_path.exists():
        return Result[Unit].err(LMSError("The save path entered does not exist"))

    table.settings.data_dir = str(data_path)
    print(f"Data Path has been successfully initialized to {data_path}")
    return Result[Unit].unit()


def input_course_name(config: Config) -> Result[Unit]:
    from pylms.cli import input_option

    result = input_option(COURSES, prompt="Select the course name")
    if result.is_err():
        return Result[Unit].err(result.unwrap_err())
    _, course_name = result.unwrap()
    print(f"\nYou have selected {course_name}\n")
    config.settings.course_name = course_name
    return Result[Unit].unit()

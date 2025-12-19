from pathlib import Path

from ..config import Config
from ..constants import COURSES, DEFAULT_DATA_PATH
from ..errors import Result, Unit
from ..info import printpass
from .option_input import input_option
from .path_input import input_path


def input_dir(config: Config) -> Result[Unit]:
    save_path = Path(config.settings.data_dir)
    if save_path.exists() and save_path != Path(""):
        print(f"Data Path has been successfully initialized to {save_path}")
        return Result.unit()
    result: Result[Path] = input_path(
        "Enter the location to save files to. Enter the letter 's' to skip. [Ensure that the location has no file called 'data']: "
    )
    if result.is_err():
        return result.propagate()
    data_dir: Path = result.unwrap()

    if data_dir.name.lower() == "s":
        print("Skipping Data Path setup")
        print(f"Data Path not set. Defaulting to {DEFAULT_DATA_PATH}")
        config.settings.data_dir = str(DEFAULT_DATA_PATH)
        return Result.unit()

    if not data_dir.is_dir():
        return Result.err("The save path entered is not a directory")

    for each_item in data_dir.iterdir():
        each_path: Path = Path(each_item)
        if each_path.is_dir() and each_path.name == "data":
            return Result.err(
                "The save path entered contains a directory called 'data'"
            )

    if not data_dir.exists():
        return Result.err("The save path entered does not exist")

    config.settings.data_dir = str(data_dir)
    printpass(f"Data Path has been successfully initialized to {data_dir}")
    return Result.unit()


def input_course_name(config: Config) -> Result[Unit]:
    result = input_option(COURSES, prompt="Select the course name")
    if result.is_err():
        return result.propagate()

    _, course_name = result.unwrap()

    printpass(f"You have selected {course_name}\n")
    config.settings.course_name = course_name
    return Result.unit()

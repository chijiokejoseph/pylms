from pathlib import Path
from typing import Callable

from pylms.cli.custom_inputs import input_str
from pylms.cli.errors import InvalidPathError
from pylms.errors import Result


def input_path(
    msg: str,
    str_test_fn: Callable[[str], bool] = lambda x: True,
    path_test_fn: Callable[[Path], bool] = lambda x: True,
    str_test_diagnosis: str | None = None,
    path_test_diagnosis: str | None = None,
    trials: int = 3,
) -> Result[Path]:
    """
    Prompt the user to input a path string, validate it, and return a Path object.

    :param msg: (str) - The prompt message to display to the user.
    :param str_test_fn: (Callable[[str], bool]) - Function to validate the input string.
    :param path_test_fn: (Callable[[Path], bool]) - Function to validate the Path object.
    :param str_test_diagnosis: (str | None) - Optional diagnosis message for string validation failure.
    :param path_test_diagnosis: (str | None) - Optional diagnosis message for path validation failure.
    :param trials: (int) - Number of allowed input attempts.

    :return: (Result[Path]) - A result containing the validated Path object.
    :rtype: Result[Path]

    :raises InvalidPathError: If the input path does not meet validation criteria.
    """
    # Prompt user for input string with validation
    result: Result[str] = input_str(
        msg, str_test_fn, str_test_diagnosis, trials, lower_case=False
    )
    if result.is_err():
        return Result[Path].err(result.unwrap_err())
    path_str: str = result.unwrap()
    # Strip whitespace and remove surrounding quotes
    path_str = path_str.strip()
    path_str = path_str.removesuffix('"')
    path_str = path_str.removesuffix("'")
    path_str = path_str.removeprefix('"')
    path_str = path_str.removeprefix("'")
    # Convert string to Path object
    path: Path = Path(path_str)
    # Validate the Path object
    if not path_test_fn(path):
        diagnosis = (
            f"\nInput Path: '{path}', diagnosis: {path_test_diagnosis}"
            if path_test_diagnosis is not None
            else ""
        )
        err_msg: str = f"'{path_str}' does not meet input requirements. {diagnosis}"
        # Raise error if validation fails
        raise InvalidPathError(err_msg)
    # Return the validated Path object
    return Result[Path].ok(path)


def test_path_in(path_input: Path) -> bool:
    """
    Validate that the given path is an absolute path pointing to an Excel file that exists.

    :param path_input: (Path) - The path to validate.
    :type path_input: Path

    :return: (bool) - True if the path is absolute, points to an Excel file, and exists; False otherwise.
    :rtype: bool
    """
    # Check if the path is absolute
    if not path_input.is_absolute():
        print(f"{path_input} is not absolute")
        return False
    # Check if the file has an Excel extension
    if not path_input.name.endswith("xlsx"):
        print(f"{path_input} does not point to an excel file")
        return False
    # Check if the path exists
    return path_input.exists()

from pathlib import Path
from typing import Callable

from ..errors import Result, eprint
from .custom_inputs import input_str


def input_path(
    msg: str,
    str_test_fn: Callable[[str], bool] = lambda x: True,
    str_test_diagnosis: str | None = None,
    trials: int = 3,
) -> Result[Path]:
    """Prompt for a filesystem path string and validate it, returning a Path.

    Prompts the user with `msg` and validates the raw input string using
    `input_str` with the provided `str_test_fn` and `str_test_diagnosis`. The
    entered string is stripped of surrounding whitespace and quotes, converted
    to a `Path`, and further validated by `test_path_in`. If validation fails,
    an error `Result` is returned describing the failure.

    Args:
        msg (str): Prompt message shown to the user.
        str_test_fn (Callable[[str], bool]): Callable used to validate the raw
            input string. Defaults to a function accepting any string.
        str_test_diagnosis (str | None): Optional message to display when the
            `str_test_fn` validation fails.
        trials (int): Number of allowed input attempts.

    Returns:
        Result[Path]: `Result.ok` with a validated `Path` on success, or
            `Result.err` with a diagnostic message when validation fails.
    """
    # Prompt user for input string with validation
    result = input_str(msg, str_test_fn, str_test_diagnosis, trials, lower_case=False)
    if result.is_err():
        return result.propagate()

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
    test, remark = test_path_in(path)

    if not test:
        diagnosis = f"\nInput Path: '{path}', diagnosis: '{remark}'"
        msg = f"'{path_str}' does not meet input requirements. {diagnosis}"

        # Return Result with error if validation fails
        eprint(f"{msg}\n")
        return Result.err(msg)

    # Return the validated Path object
    return Result.ok(path)


def test_path_in(path_input: Path) -> tuple[bool, str]:
    """Validate that a Path is absolute and exists.

    Performs basic checks that `path_input` is absolute and that the path
    exists on the filesystem. Returns a tuple where the boolean indicates
    whether the path is valid and the string provides a diagnostic message
    when the check fails.

    Args:
        path_input (Path): The path to validate.

    Returns:
        tuple[bool, str]: `(True, "")` when the path is valid; otherwise
            `(False, <diagnostic message>)`.
    """
    # Check if the path is absolute
    if not path_input.is_absolute():
        return False, f"{path_input} is not absolute"

    # Check if the path exists
    if not path_input.exists():
        return False, f"{path_input} does not exist"

    return True, ""

"""Interactive search for students by file path."""

from pylms.query_data.select_path import select_path

from ..cli import input_bool, input_path
from ..data import DataStore, print_polar
from ..errors import ForcedExitError, Result, eprint
from ..info import print_info, printpass


def search_path(ds: DataStore) -> Result[list[int]]:
    """Search for students by reading serial numbers from file.

    Supports .txt, .csv (one serial per line) and .xlsx (first numeric column).
    Loops until successful selection or ForcedExitError.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    # Loop until valid file or forced exit
    while True:
        # Prompt for file path
        print_info("Enter path to file containing serial numbers")
        result = input_path("File path: ")
        if result.is_err():
            err = result.unwrap_err()
            # Check for forced exit
            if isinstance(err, ForcedExitError):
                return result.propagate()
            result.print_if_err()
            continue

        # Get file path
        path = result.unwrap()
        result = select_path(ds, path)
        if result.is_err():
            result.print_if_err()
            continue

        selections = result.unwrap()
        serials = [val[0] for val in selections]
        print_polar(ds, serials)

        confirm = input_bool("Confirm this selection?")
        if confirm.is_err() and isinstance(confirm.error, ForcedExitError):
            return confirm.propagate()
        elif confirm.is_err():
            confirm.print_if_err()
            continue

        if not confirm.unwrap():
            eprint("Selection not confirmed")
            continue

        printpass(f"Selected {len(serials)} student(s)")
        return Result.ok([s for s, _ in selections])

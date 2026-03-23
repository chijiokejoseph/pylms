"""Interactive search for students by internship category."""

from ..cli import input_bool, input_option
from ..constants import PROGRAMS
from ..data import DataStore, print_polar
from ..errors import ForcedExitError, Result, eprint
from ..info import print_info, printpass
from .select_internship import select_internship


def search_internship(ds: DataStore) -> Result[list[int]]:
    """Search for students by internship category.

    Loops until successful selection or ForcedExitError.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    while True:
        result = input_option(PROGRAMS, prompt="Select internship category")
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            result.print_if_err()
            continue

        _, category = result.unwrap()

        filter_result = select_internship(ds, category)
        if filter_result.is_err():
            filter_result.print_if_err()
            continue

        selections = filter_result.unwrap()
        print_info(f"Found {len(selections)} student(s) in category '{category}'")
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

        printpass(f"Selected {len(selections)} student(s) from category '{category}'")
        return Result.ok([serial for serial, _ in selections])

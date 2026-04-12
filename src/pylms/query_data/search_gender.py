"""Interactive search for students by gender."""

from ..cli import input_bool, input_option
from ..data import DataStore, print_ds_subset
from ..errors import ForcedExitError, Result, eprint
from ..info import print_info, printpass
from .select_gender import select_gender


def search_gender(ds: DataStore) -> Result[list[int]]:
    """Search for students by gender.

    Loops until successful selection or ForcedExitError.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    while True:
        result = input_option(["Male", "Female"], prompt="Select gender")
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            result.print_if_err()
            continue

        _, gender = result.unwrap()

        filter_result = select_gender(ds, gender)
        if filter_result.is_err():
            filter_result.print_if_err()
            continue

        selections = filter_result.unwrap()
        print_info(f"Found {len(selections)} {gender} student(s)")
        serials = [val[0] for val in selections]
        print_ds_subset(ds, serials)

        confirm = input_bool("Confirm this selection?")
        if confirm.is_err() and isinstance(confirm.error, ForcedExitError):
            return confirm.propagate()
        elif confirm.is_err():
            confirm.print_if_err()
            continue

        if not confirm.unwrap():
            eprint("Selection not confirmed")
            continue

        printpass(f"Selected {len(selections)} {gender} student(s)")
        return Result.ok([serial for serial, _ in selections])

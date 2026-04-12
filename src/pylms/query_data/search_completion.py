"""Interactive search for students by completion date."""

from ..cli import input_bool, input_str
from ..data import DataStore, print_ds_subset
from ..errors import ForcedExitError, Result, eprint
from ..info import print_info, printpass
from .select_completion import select_completion


def search_completion(ds: DataStore) -> Result[list[int]]:
    """Search for students by completion date.

    Loops until successful selection or ForcedExitError.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    while True:
        print_info("Enter completion (e.g., 'June', '6', or 'June,July')")
        result = input_str("Completion: ", lower_case=False)
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            result.print_if_err()
            continue

        query = result.unwrap()

        filter_result = select_completion(ds, query)
        if filter_result.is_err():
            filter_result.print_if_err()
            continue

        selections = filter_result.unwrap()
        print_info(f"Found {len(selections)} student(s) with completion '{query}'")
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

        printpass(f"Selected {len(selections)} student(s) with completion '{query}'")
        return Result.ok([serial for serial, _ in selections])

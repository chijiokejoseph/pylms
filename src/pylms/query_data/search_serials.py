"""Interactive search for students by serial numbers."""

from ..cli import input_bool, input_str
from ..cli_utils import parse_nums
from ..data import DataStore, print_ds, print_ds_subset
from ..errors import ForcedExitError, Result, eprint
from ..info import print_info, printpass
from .select_serials import select_serials


def search_serials(ds: DataStore) -> Result[list[int]]:
    """Search for students by directly entering serial numbers.

    Loops until successful selection or ForcedExitError.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    while True:
        print_info("Student Records are shown below")
        print_ds(ds)
        print_info("Enter serial numbers (comma-separated, e.g., 1,5,10-15,20)")
        result = input_str("Serial numbers: ", lower_case=False)
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            result.print_if_err()
            continue

        serials_str = result.unwrap()

        serials_result = parse_nums(serials_str)
        if serials_result.is_err():
            serials_result.print_if_err()
            continue

        serials = serials_result.unwrap()
        if len(serials) == 0:
            eprint("No serial numbers entered")
            continue

        selection_result = select_serials(ds, serials)
        if selection_result.is_err():
            selection_result.print_if_err()
            continue

        selections = selection_result.unwrap()
        serials = [val[0] for val in selections]
        print_ds_subset(ds, serials)
        # print_selection(selection)

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
        return Result.ok(serials)

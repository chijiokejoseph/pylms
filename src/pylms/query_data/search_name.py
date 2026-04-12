"""Interactive search for students by name."""

from ..cli import input_bool, input_str
from ..cli_utils import parse_nums
from ..data import DataStore, print_ds_subset
from ..errors import ForcedExitError, Result, eprint
from ..info import print_info, printpass
from .select_name import select_name
from .select_serials import select_serials


def search_name(ds: DataStore) -> Result[list[int]]:
    """Search for students by name and select from results.

    Loops until successful selection or ForcedExitError.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with selected serial numbers or ForcedExitError.
    """
    while True:
        result = input_str("Enter name to search: ", lower_case=False)
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            result.print_if_err()
            continue

        query = result.unwrap()

        matches_result = select_name(ds, query)
        if matches_result.is_err():
            matches_result.print_if_err()
            continue

        matches = matches_result.unwrap()
        print_info(f"Found {len(matches)} matching student(s)")
        serials = [val[0] for val in matches]
        print_ds_subset(ds, serials)
        # print_selection(matches)

        result = input_str("Enter serial numbers (comma-separated): ", lower_case=False)
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

        match_serials = {serial for serial, _ in matches}
        invalid = [s for s in serials if s not in match_serials]
        if len(invalid) > 0:
            eprint(
                f"Serial numbers {invalid} not in search results. "
                + f"Valid serials: {sorted(match_serials)}"
            )
            continue

        selection_result = select_serials(ds, serials)
        if selection_result.is_err():
            selection_result.print_if_err()
            continue

        selections = selection_result.unwrap()
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

        printpass(f"Selected {len(serials)} student(s)")
        return Result.ok(serials)

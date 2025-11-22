from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import save
from pylms.errors import eprint
from pylms.history import History
from pylms.info import println, printpass
from pylms.lms import (
    collate_merit,
    collate_result,
    edit_result,
    overwrite_result,
    view_result,
)
from pylms.utils import DataStore


def run_result_lms(ds: DataStore, history: History) -> None:
    """
    Interactive menu for managing LMS results.

    Presents a command-line menu to the user for performing various result-related
    operations on the provided DataStore. The available actions include collating,
    viewing, editing, and overwriting results. After each operation, changes are
    saved to both the DataStore and the History.

    :param ds: (DataStore) - The data store instance containing LMS data.
    :type ds: DataStore
    :param history: (History) - The history object for tracking and saving changes.
    :type history: History

    :return: (None) - This function does not return a value.
    :rtype: None
    """
    menu: list[str] = [
        "Collate Results",
        "View Results",
        "Edit Results",
        "Overwrite Results",
        "Return to Previous Menu",
    ]

    while True:
        selection_result = interact(menu)
        if selection_result.is_err():
            eprint(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match selection:
            case 1:
                result = collate_result(ds, history)
                if result.is_err():
                    continue
                printpass("Results collated successfully")
            case 2:
                view_result(ds)
                print()
            case 3:
                result = edit_result(ds)
                if result.is_err():
                    continue
                result = collate_merit(ds, history)
                if result.is_err():
                    continue
                printpass("Result edited successfully\n")
            case 4:
                result = overwrite_result(ds)
                if result.is_err():
                    continue
                println("Results overwritten, now recollating...")
                result = collate_merit(ds, history)
                if result.is_err():
                    continue
                printpass("Result overwritten successfully\n")
            case 5:
                break
            case _:
                pass

        save(ds)
        history.save()

    return None

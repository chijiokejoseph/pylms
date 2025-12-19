from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import save
from ..history import History, save_history
from ..info import print_info, printpass
from ..result_collate import (
    collate_merit,
    collate_result,
)
from ..result_edit import (
    edit_result,
    overwrite_result,
)
from ..result_utils import view_result


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
        selection = interact(menu)
        if selection.is_err():
            continue

        selection = selection.unwrap()

        cmd: str = menu[selection - 1]

        if selection < len(menu):
            result = cache_for_cmd(cmd)
            if result.is_err():
                continue

        match selection:
            case 1:
                result = collate_result(history)
                if result.is_err():
                    continue
                printpass("Results collated successfully")
            case 2:
                result = view_result(ds)
                if result.is_err():
                    continue

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

                print_info("Results overwritten, now recollating...")

                result = collate_merit(ds, history)
                if result.is_err():
                    continue

                printpass("Result overwritten successfully\n")
            case 5:
                break
            case _:
                pass

        result = save(ds)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

        result = save_history(history)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

    return None

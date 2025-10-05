from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.lms import (
    collate_result,
    edit_result,
    collate_merit,
    overwrite_result,
    view_result,
)
from pylms.data_ops import save
from pylms.history import History
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
            print(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match int(selection):
            case 1:
                # app_ds = load()
                # collate_result(app_ds, history)
                collate_result(ds, history)
            case 2:
                # app_ds = load()
                # view_result(app_ds)
                view_result(ds)
                print()
            case 3:
                # app_ds = load()
                # edit_result(app_ds)
                # collate_merit(app_ds)
                result = edit_result(ds)
                if result.is_err():
                    continue
                collate_merit(ds)
                print("\nResult edited successfully\n")
            case 4:
                # app_ds = load()
                # overwrite_result(app_ds)
                # collate_merit(app_ds)
                overwrite_result(ds)
                collate_merit(ds)
                print("\nResult overwritten successfully\n")
            case 5:
                break
            case _:
                pass
                # app_ds = load()
        # save(app_ds)
        save(ds)
        history.save()

    return None

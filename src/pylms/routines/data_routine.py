from pylms.cache import cache_for_cmd, rollback_to_cmd
from pylms.cli import interact
from pylms.data_ops import edit, list_ds, load, remove_students, save, view
from pylms.errors import eprint
from pylms.info import printpass
from pylms.utils import DataStore


def handle_data(ds: DataStore) -> None:
    menu: list[str] = [
        "View Students' Data",
        "Edit Students' Data",
        "Print Students Data to Excel",
        "Delete Students' Data",
        "Rollback Data",
        "Return to Main Menu",
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
                view(ds)
            case 2:
                result = edit(ds)
                if result.is_err():
                    continue
                printpass("Edited Datastore successfully")
            case 3:
                list_ds(ds)
            case 4:
                remove_students(ds)
                printpass("Students removed successfully\n")
            case 5:
                rollback_to_cmd()
                ds.copy_from(load())
            case _:
                break

        save(ds)

    return None

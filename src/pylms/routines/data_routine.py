from pylms.cache import cache_for_cmd, rollback_to_cmd
from pylms.cli import interact
from pylms.data_ops import edit, list_ds, remove_students, save, view, load
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
        selection: int = interact(menu)
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match int(selection):
            case 1:
                # app_ds = load()
                # view(app_ds)
                ds.raise_for_status()
                view(ds)
            case 2:
                # app_ds = load()
                # app_ds = edit(app_ds)
                ds.raise_for_status()
                edit(ds)
            case 3:
                # app_ds = load()
                # list_ds(app_ds)
                ds.raise_for_status()
                list_ds(ds)
            case 4:
                # app_ds = load()
                # app_ds = remove_students(app_ds)
                ds.raise_for_status()
                remove_students(ds)
                print("Students removed successfully\n")
            case 5:
                ds.raise_for_status()
                rollback_to_cmd()
                ds.copy_from(load())
                # app_ds = load()
            case _:
                break

        save(ds)

    return None

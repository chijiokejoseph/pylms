from ..cache import cache_for_cmd, rollback_to_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import edit, list_ds, load, remove_students, save, view
from ..info import print_info, printpass


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
                result = view(ds)
                if result.is_err():
                    continue
            case 2:
                result = edit(ds)
                if result.is_err():
                    continue
                printpass("Edited Datastore successfully")
            case 3:
                result = list_ds(ds)
                if result.is_err():
                    continue

            case 4:
                result = remove_students(ds)
                if result.is_err():
                    continue
                printpass("Students removed successfully\n")
            case 5:
                result = rollback_to_cmd()
                if result.is_err():
                    continue

                app_ds = load()
                if app_ds.is_err():
                    continue

                app_ds = app_ds.unwrap()
                ds.copy_from(app_ds)

                printpass("Rollback completed successfully")
            case _:
                break

        result = save(ds)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

    return None

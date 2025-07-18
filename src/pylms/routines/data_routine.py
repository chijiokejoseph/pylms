from pylms.state import cache_for_cmd, rollback_to_cmd
from pylms.cli import interact
from pylms.data_ops import edit, load, record, remove_students, save, view


def handle_data() -> None:
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
                app_ds = load()
                view(app_ds)
            case 2:
                app_ds = load()
                app_ds = edit(app_ds)
            case 3:
                app_ds = load()
                record(app_ds)
            case 4:
                app_ds = load()
                app_ds = remove_students(app_ds)
                print("Students removed successfully\n")
            case 5:
                rollback_to_cmd()
                app_ds = load()
            case _:
                break

        save(app_ds)

    return None

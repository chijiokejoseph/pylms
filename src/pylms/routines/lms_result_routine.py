from pylms.state import cache_for_cmd
from pylms.cli import interact
from pylms.lms import (
    collate_result,
    edit_result,
    collate_merit,
    overwrite_result,
    view_result,
)
from pylms.data_ops import load, save
from pylms.state import History


def run_result_lms(history: History) -> None:
    menu: list[str] = [
        "Collate Results",
        "View Results",
        "Edit Results",
        "Overwrite Results",
        "Return to Previous Menu",
    ]

    while True:
        selection: int = interact(menu)
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match int(selection):
            case 1:
                app_ds = load()
                collate_result(app_ds, history)
            case 2:
                app_ds = load()
                view_result(app_ds)
                print()
            case 3:
                app_ds = load()
                edit_result(app_ds)
                collate_merit(app_ds)
                print("\nResult edited successfully\n")
            case 4:
                app_ds = load()
                overwrite_result(app_ds)
                collate_merit(app_ds)
                print("\nResult overwritten successfully\n")
            case 5:
                break
            case _:
                app_ds = load()
        save(app_ds)
        history.save()

    return None

from pylms.state import cache_for_cmd
from pylms.cli import interact
from pylms.lms import (
    collate_fast_track,
    collate_merge,
    collate_result,
    edit_result,
    group,
    collate_merit,
    overwrite_result,
    view_result,
)
from pylms.data_ops import load, save
from pylms.utils import DataStore


def run_lms() -> None:
    menu: list[str] = [
        "Group Students",
        "Collate Results",
        "View Results",
        "Edit Results",
        "Overwrite Results",
        "Collate Fast Track Awardees",
        "Collate Merit Awardees",
        "Merge Fast Track and Merit Awardees",
        "Return to Main Menu",
    ]

    while True:
        selection: int = interact(menu)
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match int(selection):
            case 1:
                app_ds: DataStore = load()
                group(app_ds)
                print("Students have been grouped successfully\n")
            case 2:
                app_ds = load()
                collate_result(app_ds)
                print("\nResult collated successfully\n")
            case 3:
                app_ds = load()
                view_result(app_ds)
                print()
            case 4:
                app_ds = load()
                edit_result(app_ds)
                collate_merit(app_ds)
                print("\nResult edited successfully\n")
            case 5:
                app_ds = load()
                overwrite_result(app_ds)
                collate_merit(app_ds)
                print("\nResult overwritten successfully\n")
            case 6:
                app_ds = load()
                app_ds = collate_fast_track(app_ds)
                print("Recorded Fast Track Awardees.\n")
            case 7:
                app_ds = load()
                collate_merit(app_ds)
                print("Recorded Merit Awardees.\n")
            case 8:
                app_ds = load()
                collate_merge(app_ds)
                print("\nMerit and Fast Track Awardees merged successfully\n")
            case 9:
                break
            case _:
                app_ds = load()
        save(app_ds)

    return None

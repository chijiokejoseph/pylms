from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.lms import (
    group,
)
from pylms.routines.lms_awardees_routine import run_awardees_lms
from pylms.routines.lms_result_routine import run_result_lms
from pylms.routines.lms_collate_routine import run_collate_lms
from pylms.data_ops import save
from pylms.history import History
from pylms.utils import DataStore


def run_lms(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Group Students",
        "Collate Student Metrics",
        "Manage Results",
        "Manage Awardees",
        "Return to Main Menu",
    ]

    while True:
        selection: int = interact(menu)
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match int(selection):
            case 1:
                # app_ds: DataStore = load()
                # group(app_ds)
                ds.raise_for_status()
                group(ds)
                print("Students have been grouped successfully\n")
            case 2:
                # app_ds = load()
                ds.raise_for_status()
                run_collate_lms(ds, history)
            case 3:
                # app_ds = load()
                ds.raise_for_status()
                run_result_lms(ds, history)
            case 4:
                # app_ds = load()
                ds.raise_for_status()
                run_awardees_lms(ds, history)
            case 5:
                break
            case _:
                pass
                # app_ds = load()
        # save(app_ds)
        save(ds)
        history.save()

    return None

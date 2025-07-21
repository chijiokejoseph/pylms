from pylms.state import cache_for_cmd
from pylms.cli import interact
from pylms.lms import (
    collate_fast_track,
    collate_merge,
    collate_merit,
)
from pylms.data_ops import save
from pylms.state import History
from pylms.utils import DataStore


def run_awardees_lms(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Collate Fast Track Awardees",
        "Collate Merit Awardees",
        "Merge Fast Track and Merit Awardees",
        "Return to Previous Menu",
    ]

    ds.raise_for_status()
    while True:
        selection: int = interact(menu)
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match int(selection):
            case 1:
                # app_ds: DataStore = load()
                # app_ds = collate_fast_track(app_ds)
                collate_fast_track(ds)
                print("Recorded Fast Track Awardees.\n")
            case 2:
                # app_ds = load()
                # collate_merit(app_ds)
                collate_merit(ds)
                print("Recorded Merit Awardees.\n")
            case 3:
                # app_ds = load()
                # collate_merge(app_ds)
                collate_merge(ds)
                print("\nMerit and Fast Track Awardees merged successfully\n")
            case 4:
                break
            case _:
                pass
                # app_ds = load()
        # save(app_ds)
        save(ds)
        history.save()

    return None

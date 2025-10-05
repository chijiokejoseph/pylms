from pylms.history import History
from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.lms.collate import collate_assessment, collate_attendance, collate_project
from pylms.utils import DataStore
from pylms.data_ops import save


def run_collate_lms(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Collate Attendance",
        "Collate Assessment",
        "Collate Project",
        "Return to Previous Menu",
    ]

    ds.raise_for_status()
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
                # app_ds: DataStore = load()
                # collate_attendance(app_ds, history)
                collate_attendance(ds, history)
            case 2:
                # app_ds = load()
                collate_assessment(history)
            case 3:
                # app_ds = load()
                collate_project(history)
            case 4:
                break
            case _:
                pass
                # app_ds = load()
        # save(app_ds)
        save(ds)
        history.save()
    return None

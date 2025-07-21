from pylms.history import History
from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.lms.collate import (
    collate_assessment,
    collate_attendance,
    collate_project
)
from pylms.utils import DataStore
from pylms.data_ops import load, save


def run_collate_lms(history: History) -> None:
    menu: list[str] = [
        "Collate Attendance",
        "Collate Assessment",
        "Collate Project",
        "Return to Previous Menu",
    ]

    while True:
        selection: int = interact(menu)
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match int(selection):
            case 1:
                app_ds: DataStore = load()
                collate_attendance(app_ds, history)
                print(f"\n{history.has_collated_attendance = }\n")
            case 2:
                app_ds = load()
                collate_assessment(history)
            case 3:
                app_ds = load()
                collate_project(history)
            case 4:
                break
            case _:
                app_ds = load()
        save(app_ds)
        history.save()
    return None
                
    
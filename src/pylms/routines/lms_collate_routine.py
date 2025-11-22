from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import save
from pylms.errors import eprint
from pylms.history import History
from pylms.info import printpass
from pylms.lms.collate import collate_assessment, collate_attendance, collate_project
from pylms.utils import DataStore


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
            eprint(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match selection:
            case 1:
                result = collate_attendance(ds, history)
                if result.is_err():
                    continue
                printpass("Attendance collated successfully")
            case 2:
                collate_assessment(history)
            case 3:
                collate_project(history)
            case 4:
                break
            case _:
                pass

        save(ds)
        history.save()
    return None

from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import save_ds
from ..history import History, save_history
from ..info import print_info, printpass
from ..result_collate import collate_assessment, collate_attendance, collate_project
from ..config import Config


def run_collate_lms(config: Config, ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Collate Attendance",
        "Collate Assessment",
        "Collate Project",
        "Return to Previous Menu",
    ]

    while True:
        selection = interact(menu)
        if selection.is_err():
            continue

        selection = selection.unwrap()

        cmd: str = menu[selection - 1]

        if selection < len(menu):
            result = cache_for_cmd(config, cmd)
            if result.is_err():
                continue

        match selection:
            case 1:
                result = collate_attendance(config, ds, history)
                result.print_if_err()
                if result.is_err():
                    continue
                printpass("Attendance collated successfully")
            case 2:
                result = collate_assessment(config, history)
                result.print_if_err()
                if result.is_err():
                    continue

                printpass("Assessment collated successfully")
            case 3:
                result = collate_project(config, history)
                result.print_if_err()
                if result.is_err():
                    continue

                printpass("Project collated successfully")
            case 4:
                break
            case _:
                pass

        result = save_ds(config, ds)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

        result = save_history(config, history)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )
    return None

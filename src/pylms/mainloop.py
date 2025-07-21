import traceback
from typing import Callable
from pylms.state import cache_for_cmd
from pylms.cli import interact, input_option
from pylms.errors import LMSError
from pylms.data_ops import load, view
from pylms.lms.collate import view_result
from pylms.routines import (
    handle_cds,
    handle_cohort,
    handle_data,
    handle_rollcall,
    register,
    run_lms,
)
from pylms.history import History
from pylms.utils import DataStore


def handle_err[K](func: Callable[[], K]) -> K | None:
    try:
        return func()
    except LMSError as e:
        idx, choice = input_option(["Yes", "No"], prompt="Do you wish to view error trace")
        choice = choice.lower()
        if idx == 0:
            traceback.print_exc()
        print(e.message)
    print("\n")
    return None
    


def mainloop() -> bool:
    menu: list[str] = [
        "Attendance",
        "CDS",
        "Cohort",
        "Data Records",
        "LMS",
        "Register",
        "Quit",
    ]
    history: History = History.load()
    ds: DataStore = load()
    selection: int = interact(menu)
    cmd: str = menu[selection - 1]
    if selection < len(menu):
        cache_for_cmd(cmd)
    match int(selection):
        case 1:
            handle_rollcall(ds, history)
        case 2:
            handle_cds(ds, history)
        case 3:
            handle_cohort()
        case 4:
            handle_data(ds)
        case 5:
            run_lms(ds, history)
        case 6:
            register(ds, history)
        case _:
            print(
                "Hello friend, Jayce 🎓 again, I hope I have helped you a lot today. See you again next time!"
            )
            return False
    return True


def closed_loop() -> bool:
    print("\nCohort is closed.\n")
    menu: list[str] = [
        "View Data Records",
        "View Results",
        "Cohort",
        "Quit",
    ]
    selection: int = interact(menu)
    match int(selection):
        case 1:
            app_ds = load()
            view(app_ds)
        case 2:
            app_ds = load()
            view_result(app_ds)
        case 3:
            handle_cohort()
        case _:
            print(
                "Hello friend, Jayce 🎓 again, I hope I have helped you a lot today. See you again next time!"
            )
            return False
    return True

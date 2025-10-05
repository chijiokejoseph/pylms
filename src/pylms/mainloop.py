import traceback
from typing import Callable
from pylms.cache import cache_for_cmd
from pylms.cli import interact, input_option
from pylms.errors import LMSError, Result
from pylms.data_ops import load, view
from pylms.lms.collate import view_result
from pylms.routines import (
    handle_cds,
    handle_cohort,
    handle_data,
    handle_rollcall,
    handle_message,
    register,
    run_lms,
)
from pylms.history import History
from pylms.utils import DataStore
from pylms.config import Config


def handle_err(func: Callable[[], Result[bool]]) -> bool | None:
    try:
        result = func()
        if result.is_err():
            return None
        return result.unwrap()
    except LMSError as e:
        option_result = input_option(
            ["Yes", "No"], prompt="Do you wish to view error trace"
        )
        if option_result.is_err():
            print(f"Error retrieving option: {option_result.unwrap_err()}")
            return None
        idx, choice = option_result.unwrap()
        choice = choice.lower()
        if idx == 1:
            traceback.print_exc()
        print(e.message)
    print("\n")
    return None


def mainloop(config: Config) -> Result[bool]:
    menu: list[str] = [
        "Attendance",
        "CDS",
        "Cohort",
        "Data Records",
        "LMS",
        "Register",
        "Message",
        "Quit",
    ]
    history: History = History.load()
    ds: DataStore = load()
    selection_result = interact(menu)
    if selection_result.is_err():
        return Result[bool].err(selection_result.unwrap_err())
    selection: int = selection_result.unwrap()
    cmd: str = menu[selection - 1]
    if selection < len(menu):
        cache_for_cmd(cmd)
    match int(selection):
        case 1:
            handle_rollcall(ds, history)
        case 2:
            handle_cds(ds, history)
        case 3:
            handle_cohort(config)
        case 4:
            handle_data(ds)
        case 5:
            run_lms(ds, history)
        case 6:
            register(ds, history)
        case 7:
            handle_message(ds, history)
        case _:
            print(
                "Hello friend, Jayce 🎓 again, I hope I have helped you a lot today. See you again next time!"
            )
            return Result[bool].ok(False)
    return Result[bool].ok(True)


def closed_loop(config: Config) -> Result[bool]:
    print("\nCohort is closed.\n")
    menu: list[str] = [
        "View Data Records",
        "View Results",
        "Cohort",
        "Quit",
    ]
    selection_result = interact(menu)
    if selection_result.is_err():
        return Result[bool].err(selection_result.unwrap_err())
    selection: int = selection_result.unwrap()
    match int(selection):
        case 1:
            app_ds = load()
            view(app_ds)
        case 2:
            app_ds = load()
            view_result(app_ds)
        case 3:
            handle_cohort(config)
        case _:
            print(
                "Hello friend, Jayce 🎓 again, I hope I have helped you a lot today. See you again next time!"
            )
            return Result[bool].ok(False)
    return Result[bool].ok(True)

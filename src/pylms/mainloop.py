import traceback
from typing import Callable

from .cache import cache_for_cmd
from .cli import input_bool, interact
from .config import Config
from .data_service import load, view
from .errors import LMSError, Result, eprint
from .history import load_history
from .info import print_info
from .result_utils import view_result
from .routines import (
    handle_cds,
    handle_cohort,
    handle_data,
    handle_message,
    handle_rollcall,
    register,
    run_lms,
)


def handle_err(func: Callable[[], Result[bool]]) -> bool | None:
    try:
        result = func()
        if result.is_err():
            return None
        return result.unwrap()
    except LMSError as e:
        result = input_bool(prompt="Do you wish to view error trace")
        if result.is_err():
            return None
        choice = result.unwrap()
        if choice:
            traceback.print_exc()
        eprint(e.message)
    print("\n")
    return None


def mainloop(config: Config) -> Result[bool]:
    menu = [
        "Attendance",
        "CDS",
        "Cohort",
        "Data Records",
        "LMS",
        "Register",
        "Message",
        "Quit",
    ]

    history = load_history()
    if history.is_err():
        return history.propagate()
    history = history.unwrap()

    ds = load()
    if ds.is_err():
        return ds.propagate()
    ds = ds.unwrap()

    selection = interact(menu)

    if selection.is_err():
        return selection.propagate()

    selection = selection.unwrap()

    cmd = menu[selection - 1]

    if selection < len(menu):
        result = cache_for_cmd(cmd)

        if result.is_err():
            return result.propagate()

    match selection:
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
            print_info(
                "Hello friend, Jayce 🎓 again, I hope I have helped you a lot today. See you again next time!"
            )
            return Result.ok(False)
    return Result.ok(True)


def closed_loop(config: Config) -> Result[bool]:
    print_info("Cohort is closed.\n")
    menu = [
        "View Data Records",
        "View Results",
        "Cohort",
        "Quit",
    ]
    selection = interact(menu)

    if selection.is_err():
        return selection.propagate()

    selection = selection.unwrap()

    match int(selection):
        case 1:
            app_ds = load()
            if app_ds.is_err():
                return app_ds.propagate()
            app_ds = app_ds.unwrap()

            result = view(app_ds)
            if result.is_err():
                return result.propagate()
        case 2:
            app_ds = load()

            if app_ds.is_err():
                return app_ds.propagate()
            app_ds = app_ds.unwrap()

            result = view_result(app_ds)
            if result.is_err():
                return result.propagate()

        case 3:
            handle_cohort(config)
        case _:
            print_info(
                "Hello friend, Jayce 🎓 again, I hope I have helped you a lot today. See you again next time!"
            )
            return Result.ok(False)
    return Result.ok(True)

from pylms.state import cache_for_cmd
from pylms.cli import interact
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
    selection: int = interact(menu)
    cmd: str = menu[selection - 1]
    if selection < len(menu):
        cache_for_cmd(cmd)
    match int(selection):
        case 1:
            handle_rollcall()
        case 2:
            handle_cds()
        case 3:
            handle_cohort()
        case 4:
            handle_data()
        case 5:
            run_lms()
        case 6:
            register()
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

from pylms.cli import input_option, interact
from pylms.config import new_state, read_state, write_state, AppConfig
from pylms.utils import paths, rm_path
from pylms.constants import HISTORY_PATH, GLOBAL_RECORD_PATH


def handle_cohort() -> None:
    menu: list[str] = [
        "End the Cohort",
        "Reopen the Cohort",
        "New Cohort",
        "Return to Main Menu",
    ]

    app_state: AppConfig = read_state()

    while True:
        selection: int = interact(menu)
        match int(selection):
            case 1:
                if not app_state.is_open():
                    print("\nCohort is already closed.\n")
                    continue
                choice = input_option(
                    ["Yes", "No"],
                    "End Cohort",
                    prompt="Do you wish to end the current cohort?",
                )
                if choice == "Yes":
                    app_state = read_state()
                    app_state.close()
                print("\nThe Cohort has been closed.\n")
            case 2:
                if app_state.is_open():
                    print("\nCohort is already open.\n")
                    continue
                choice = input_option(
                    ["Yes", "No"],
                    "Reopen Cohort",
                    prompt="Do you wish to reopen the closed cohort?",
                )
                if choice == "Yes":
                    app_state = read_state()
                    app_state.open()
                print("\nThe Cohort which was closed is now open.\n")
            case 3:
                if app_state.is_open():
                    print("\nClose the Cohort First before creating a new cohort.\n")
                    continue
                rm_path(paths.get_cache_path())
                rm_path(HISTORY_PATH)
                rm_path(GLOBAL_RECORD_PATH)
                app_state = new_state()
                print("\nYou have a new open cohort\n")
            case _:
                break
        write_state(app_state)
    return None

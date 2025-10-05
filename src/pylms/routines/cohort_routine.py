from pylms.cli import input_option, interact
from pylms.config import new_config, write_config, Config
from pylms.utils import paths, rm_path
from pylms.constants import HISTORY_PATH, GLOBAL_RECORD_PATH


def handle_cohort(config: Config) -> None:
    menu: list[str] = [
        "End the Cohort",
        "Reopen the Cohort",
        "New Cohort",
        "Return to Main Menu",
    ]

    while True:
        selection_result = interact(menu)
        if selection_result.is_err():
            print(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        match int(selection):
            case 1:
                if not config.is_open():
                    print("\nCohort is already closed.\n")
                    continue
                result = input_option(
                    ["Yes", "No"],
                    "End Cohort",
                    prompt="Do you wish to end the current cohort?",
                )
                if result.is_err():
                    continue
                _, choice = result.unwrap()
                if choice == "Yes":
                    config.close()
                    print("\nThe Cohort, which was previously open, has been closed.\n")
            case 2:
                if config.is_open():
                    print("\nCohort is already open.\n")
                    continue
                result = input_option(
                    ["Yes", "No"],
                    "Reopen Cohort",
                    prompt="Do you wish to reopen the closed cohort?",
                )
                if result.is_err():
                    continue
                _, choice = result.unwrap()
                if choice == "Yes":
                    config.open()
                    print("\nThe Cohort, which was previously closed, is now open.\n")
            case 3:
                if config.is_open():
                    print("\nClose the Cohort First before creating a new cohort.\n")
                    continue
                rm_path(paths.get_cache_path())
                rm_path(HISTORY_PATH)
                rm_path(GLOBAL_RECORD_PATH)
                config.from_self(new_config())
                print("\nYou have a new open cohort\n")
            case _:
                break
        write_config(config)
    return None

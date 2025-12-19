from ..cli import input_option, interact
from ..config import Config, new_config, write_config
from ..constants import GLOBAL_RECORD_PATH, HISTORY_PATH
from ..info import print_info, printpass
from ..paths import get_cache_path, rm_path


def handle_cohort(config: Config) -> None:
    menu: list[str] = [
        "End the Cohort",
        "Reopen the Cohort",
        "New Cohort",
        "Return to Main Menu",
    ]

    while True:
        selection = interact(menu)
        if selection.is_err():
            continue

        selection = selection.unwrap()

        match selection:
            case 1:
                if not config.is_open():
                    print_info("Cohort is already closed.\n")
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
                    printpass(
                        "The Cohort, which was previously open, has been closed.\n"
                    )
            case 2:
                if config.is_open():
                    print_info("Cohort is already open.\n")
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
                    printpass("The Cohort, which was previously closed, is now open.\n")
            case 3:
                if config.is_open():
                    print_info("Close the Cohort First before creating a new cohort.\n")
                    continue
                result = rm_path(get_cache_path())
                if result.is_err():
                    continue

                result = rm_path(HISTORY_PATH)
                if result.is_err():
                    continue

                result = rm_path(GLOBAL_RECORD_PATH)
                if result.is_err():
                    continue

                config.from_self(new_config())
                printpass("You have a new open cohort\n")
            case _:
                break
        write_config(config)
    return None

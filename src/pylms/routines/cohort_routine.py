from ..cli import get_interlude_dates, input_option, interact
from ..config import Config, new_config, write_config
from ..constants import DATE_FMT, GLOBAL_RECORD_PATH, HISTORY_PATH
from ..data import DataStore
from ..data_service import save
from ..history import History, add_interlude, save_history
from ..info import print_info, printpass
from ..paths import get_cache_path, rm_path


def handle_cohort(config: Config, ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Add Cohort Interlude",
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
                interlude = get_interlude_dates(history)
                if interlude.is_err():
                    continue

                interlude = interlude.unwrap()
                result = add_interlude(ds, history, interlude)
                if result.is_err():
                    continue

                printpass(
                    f"Successfully added interlude starting from {interlude.start.strftime(DATE_FMT)} to {interlude.end.strftime(DATE_FMT)}"
                )

            case 2:
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
            case 3:
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
            case 4:
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

        result = save_history(history)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

        result = save(ds)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

    return None

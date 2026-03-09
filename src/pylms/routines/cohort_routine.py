from ..cli import input_bool, input_option, interact
from ..config import Config, is_open, mark_closed, mark_open, save_config
from ..constants import DATA_PATH, DATE_FMT
from ..data import DataStore
from ..data_service import save_ds
from ..history import History, add_interlude, new_interlude, save_history
from ..info import print_info, printpass
from ..paths import rm_path


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
                interlude = new_interlude(history)
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
                if not is_open(config):
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
                    mark_closed(config)
                    printpass(
                        "The Cohort, which was previously open, has been closed.\n"
                    )
            case 3:
                if is_open(config):
                    print_info("Cohort is already open.\n")
                    continue
                result = input_bool(
                    "Do you wish to reopen the closed cohort?",
                )
                if result.is_err():
                    continue
                choice = result.unwrap()
                if choice:
                    mark_open(config)
                    printpass("The Cohort, which was previously closed, is now open.\n")
            case 4:
                if is_open(config):
                    print_info("Close the Cohort First before creating a new cohort.\n")
                    continue

                result = rm_path(DATA_PATH)
                if result.is_err():
                    continue

                # convert config to hold an empty Config value
                config.copy_from(Config())

                printpass("You have a new open cohort\n")

                # return immediately to avoid trying to save data to deleted paths.
                return None
            case _:
                break
        result = save_config(config)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

        result = save_history(config, history)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

        result = save_ds(config, ds)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

    return None

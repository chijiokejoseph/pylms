from dotenv import load_dotenv

from pylms.cli import input_course_name, input_dir
from pylms.config import load, write_config
from pylms.constants import ENV_PATH
from pylms.data_service import init_ds
from pylms.errors import ForcedExitError, Result, eprint
from pylms.history import init_history
from pylms.mainloop import closed_loop, handle_err, mainloop
from pylms.paths import prepare_paths

_ = load_dotenv(ENV_PATH)


def main() -> None:
    """
    Main entry point for the application loop.

    Loads and manages the application state, prompting the user for required information
    (such as data directory and course name) if missing, prepares necessary paths, and
    runs the main or closed loop based on the application's open state. Handles errors
    gracefully and determines whether to continue running.

    Returns:
        None
    """
    run: bool = True
    while run:
        # Load the current application state from persistent storage
        config = load()

        # If the data directory is not set, prompt the user to input it and save the state
        if not config.has_data_dir():
            config_result = input_dir(config)
            if config_result.is_err():
                err = config_result.unwrap_err()
                if not isinstance(err, ForcedExitError):
                    continue
                return
            write_config(config)

        # If the course name is not set, prompt the user to input it and save the state
        if not config.has_course_name():
            course_result = input_course_name(config)
            if course_result.is_err():
                err = course_result.unwrap_err()
                if not isinstance(err, ForcedExitError):
                    continue
                return
            write_config(config)

        # Prepare any necessary file paths for the application
        prepare_paths()

        # Initialize History
        history = init_history()
        if history.is_err():
            err = history.unwrap_err()
            if isinstance(err, ForcedExitError):
                return
            eprint("Failed to save history")
            continue

        history = history.unwrap()

        # Register Data
        ds = init_ds(history)
        if ds.is_err():
            err = ds.unwrap_err()
            if isinstance(err, ForcedExitError):
                return
            eprint("Failed to register data store")
            continue

        ds = ds.unwrap()

        app_ds = ds
        app_history = history

        # Run the main loop if the application is open, otherwise run the closed loop.
        # Any exceptions are handled by handle_err.
        def func() -> Result[bool]:
            return (
                mainloop(config, app_ds, app_history)
                if config.is_open()
                else closed_loop(config, app_ds, app_history)
            )

        result = handle_err(func)

        # Determine whether to continue running based on the result of handle_err
        run = result if result is not None else True


if __name__ == "__main__":
    main()

from dotenv import load_dotenv

from pylms.config import init_config, is_open
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
        # Initialize config (loads or creates, prompts for missing data)
        config_result = init_config()
        if config_result.is_err() and isinstance(config_result.error, ForcedExitError):
            return
        elif config_result.is_err():
            eprint("Failed to initialize config")
            continue
        config = config_result.unwrap()

        # Prepare any necessary file paths for the application
        prepare_paths(config)

        # Initialize History
        history = init_history(config)
        if history.is_err() and isinstance(history.error, ForcedExitError):
            return
        elif history.is_err():
            eprint("Failed to save history")
            continue

        history = history.unwrap()

        # Register Data
        ds = init_ds(config, history)
        if ds.is_err() and isinstance(ds.error, ForcedExitError):
            return
        elif ds.is_err():
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
                if is_open(config)
                else closed_loop(config, app_ds, app_history)
            )

        result = handle_err(func)

        # Determine whether to continue running based on the result of handle_err
        run = result if result is not None else True


if __name__ == "__main__":
    main()

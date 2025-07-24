from src.pylms.mainloop import mainloop, closed_loop, handle_err
from src.pylms.utils import prepare_paths
from src.pylms.config import load, input_dir, input_course_name, write_state
from src.pylms.constants import ENV_PATH
from dotenv import load_dotenv


load_dotenv(ENV_PATH)


def main() -> None:
    """
    Main entry point for the application loop.

    Loads and manages the application state, prompting the user for required information
    (such as data directory and course name) if missing, prepares necessary paths, and
    runs the main or closed loop based on the application's open state. Handles errors
    gracefully and determines whether to continue running.

    :return: (None) - This function does not return a value.
    :rtype: None
    :raises Exception: Any exceptions raised by the called functions (such as load, input_dir,
                      input_course_name, prepare_paths, mainloop, closed_loop, or handle_err)
                      will propagate unless handled within handle_err.
    """
    run: bool = True
    while run:
        # Load the current application state from persistent storage
        app_state = load()

        # If the data directory is not set, prompt the user to input it and save the state
        if not app_state.has_data_dir():
            input_dir(app_state)
            write_state(app_state)

        # If the course name is not set, prompt the user to input it and save the state
        if not app_state.has_course_name():
            input_course_name(app_state)
            write_state(app_state)

        # Prepare any necessary file paths for the application
        prepare_paths()

        # Run the main loop if the application is open, otherwise run the closed loop.
        # Any exceptions are handled by handle_err.
        result = handle_err(
            lambda: mainloop() if app_state.is_open() else closed_loop()
        )

        # Determine whether to continue running based on the result of handle_err
        run = result if result is not None else True


if __name__ == "__main__":
    main()

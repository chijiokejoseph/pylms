from src.pylms.mainloop import mainloop, closed_loop, handle_err
from src.pylms.utils import prepare_paths
from src.pylms.config import load, input_dir, write_state
from src.pylms.constants import ENV_PATH
from dotenv import load_dotenv
load_dotenv(ENV_PATH)

def main() -> None:
    run: bool = True
    while run:
        app_state = load()
        if not app_state.has_data_dir():
            input_dir(app_state)
            write_state(app_state)
        prepare_paths()
        result = handle_err(
            lambda: mainloop() if app_state.is_open() else closed_loop()
        )
        run = result if result is not None else True


if __name__ == "__main__":
    main()

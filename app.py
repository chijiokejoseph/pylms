import traceback

from src.pylms.cli import input_str
from src.pylms.errors import LMSError
from src.pylms.mainloop import mainloop, closed_loop
from src.pylms.utils import prepare_paths
from src.pylms.state import load, input_dir, write_state


def main() -> None:
    run: bool = True
    while run:
        app_state = load()
        if not app_state.has_data_dir():
            input_dir(app_state)
            write_state(app_state)
        prepare_paths()
        try:
            run = mainloop() if app_state.is_open() else closed_loop()
        except LMSError as e:
            choice = input_str("Do you wish to view error trace ['yes' / 'y']: ")
            choice = choice.lower()
            if choice in ["yes", "y"]:
                traceback.print_exc()
            print(e.message)
        print("\n")


if __name__ == "__main__":
    main()

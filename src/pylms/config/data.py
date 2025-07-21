from pathlib import Path
from pylms.errors import LMSError
from pylms.config.app_toml import AppToml
from pylms.constants import DEFAULT_DATA_PATH


def input_fn(msg: str) -> str:
    msg += "\n[To forcefully exit the operation enter 'quit', 'exit' or 'q']: "
    user_input: str = input(msg)
    if user_input in ["quit", "exit", "q"]:
        raise LMSError("You quit the operation")
    else:
        return user_input


def input_dir(table: AppToml) -> None:
    save_path = Path(table.settings.data_dir)
    if save_path.exists() and save_path != Path(""):
        print(f"Data Path has been successfully initialized to {save_path}")
        return None
    data_dir = input_fn(
        "Enter the location to save files to. Enter the letter 's' to skip. [Ensure that the location has no file called 'data']: "
    )
    if data_dir.lower() == "s":
        print("Skipping Data Path setup")
        print(f"Data Path not set. Defaulting to {DEFAULT_DATA_PATH}")
        table.settings.data_dir = str(DEFAULT_DATA_PATH)
        return None

    data_path: Path = Path(data_dir).resolve()
    if not data_path.is_dir():
        raise LMSError("The save path entered is not a directory")
    for each_item in data_path.iterdir():
        each_path: Path = Path(each_item)
        if each_path.is_dir() and each_path.name == "data":
            raise LMSError("The save path entered contains a directory called 'data'")

    if not data_path.exists():
        raise LMSError("The save path entered does not exist")

    table.settings.data_dir = str(data_path)
    print(f"Data Path has been successfully initialized to {data_path}")
    return None

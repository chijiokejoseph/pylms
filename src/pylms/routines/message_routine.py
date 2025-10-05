from pylms.errors import Result, Unit
from pylms.utils import DataStore
from pylms.history import History
from pylms.cli import interact
from pylms.cache import cache_for_cmd
from pylms.messages import (
    custom_message_select,
    custom_message_all,
    assessment_message_all,
    update_message_select,
)


def handle_message(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Message all students with a custom message",
        "Message select students with a custom message",
        "Message all students with assessment forms",
        "Message select students with update forms",
        "Return to Previous Menu",
    ]

    while True:
        selection_result = interact(menu)
        if selection_result.is_err():
            print(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        if selection < len(menu):
            cache_for_cmd(menu[selection - 1])
        
        match int(selection):
            case 1:
                # app_ds: DataStore = load()
                # message_all_emails(app_ds, history)
                result: Result[Unit] = custom_message_all(ds)
                if result.is_err():
                    continue
            case 2:
                # app_ds = load()
                # custom_message_select_emails(app_ds, history)
                result = custom_message_select()
                if result.is_err():
                    continue
            case 3:
                result = assessment_message_all(ds, history)
                if result.is_err():
                    continue
            case 4:
                result = update_message_select(history)
                if result.is_err():
                    continue
            case _:
                break

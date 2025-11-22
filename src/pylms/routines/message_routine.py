from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.errors import Result, Unit, eprint
from pylms.history import History
from pylms.messages import (
    assessment_message_all,
    custom_message_all,
    custom_message_select,
    update_message_select,
)
from pylms.utils import DataStore


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
            eprint(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        if selection < len(menu):
            cache_for_cmd(menu[selection - 1])

        match selection:
            case 1:
                result: Result[Unit] = custom_message_all(ds)
                if result.is_err():
                    continue
            case 2:
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

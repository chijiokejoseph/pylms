from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..history import History
from ..messages import (
    assessment_message_all,
    custom_message_all,
    custom_message_select,
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
        selection = interact(menu)
        if selection.is_err():
            continue

        selection = selection.unwrap()

        cmd: str = menu[selection - 1]

        if selection < len(menu):
            result = cache_for_cmd(cmd)
            if result.is_err():
                continue

        match selection:
            case 1:
                result = custom_message_all(ds)
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

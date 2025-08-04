from pylms.utils import DataStore
from pylms.history import History
from pylms.cli import interact
from pylms.cache import cache_for_cmd
from pylms.messages import custom_message_select_emails, custom_message_all_emails


def handle_mail(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Message all student emails",
        "Message select emails",
    ]

    selection: int = interact(menu)
    if selection < len(menu):
        cache_for_cmd(menu[selection - 1])

    match int(selection):
        case 1:
            # app_ds: DataStore = load()
            # message_all_emails(app_ds, history)
            custom_message_all_emails(ds)
        case 2:
            # app_ds = load()
            # custom_message_select_emails(app_ds, history)
            custom_message_select_emails()
        case _:
            pass

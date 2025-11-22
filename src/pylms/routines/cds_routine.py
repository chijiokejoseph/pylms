from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import save
from pylms.errors import eprint
from pylms.forms.request_form_api import (
    request_cds_form,
)
from pylms.forms.retrieve_form_api import (
    retrieve_cds_form,
    save_retrieve,
)
from pylms.history import History
from pylms.info import printpass
from pylms.rollcall import (
    record_cds,
)
from pylms.utils.data import DataStore


def handle_cds(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Request CDS form",
        "Mark CDS form",
        "Return to Main Menu",
    ]

    while True:
        selection_result = interact(menu)
        if selection_result.is_err():
            eprint(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match selection:
            case 1:
                request_cds_form(ds, history)
                printpass("Generated CDS Form Successfully\n")
            case 2:
                result = retrieve_cds_form(history)
                if result.is_err():
                    eprint(
                        f"\nFailed to retrieve cds forms due to error: {result.unwrap_err()}\n"
                    )
                    continue

                cds_form_stream, info = result.unwrap()

                if cds_form_stream is not None:
                    result = record_cds(ds, cds_form_stream)
                    if result.is_err():
                        continue
                    history.add_recorded_cds_form(info)
                    save_retrieve(info)
                    printpass("Marked CDS Records")
            case _:
                break

        save(ds)
        history.save()

    return None

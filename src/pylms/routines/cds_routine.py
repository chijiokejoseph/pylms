from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import save
from ..form_request import request_cds_form
from ..form_retrieve import (
    retrieve_cds_form,
    save_retrieve,
)
from ..history import History, add_recorded_cds_form, save_history
from ..info import print_info, printpass
from ..rollcall import (
    record_cds,
)


def handle_cds(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Request CDS form",
        "Mark CDS form",
        "Return to Main Menu",
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
                request_cds_form(ds, history)
                printpass("Generated CDS Form Successfully\n")
            case 2:
                result = retrieve_cds_form(history)
                if result.is_err():
                    continue

                cds_form_stream, info = result.unwrap()

                result = record_cds(ds, cds_form_stream)
                if result.is_err():
                    continue

                add_recorded_cds_form(history, info)

                result = save_retrieve(info)
                if result.is_err():
                    continue

                printpass("Marked CDS Records")
            case _:
                break

        result = save(ds)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

        result = save_history(history)
        if result.is_err():
            print_info(
                "Last change was not saved, please rollback and repeat your last operation"
            )

    return None

from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import save
from pylms.forms.request_form_api import (
    request_cds_form,
)
from pylms.forms.retrieve_form_api import (
    retrieve_cds_form,
    save_retrieve,
)
from pylms.rollcall import (
    record_cds,
)
from pylms.history import History
from pylms.utils.data import DataStore


def handle_cds(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Request CDS form",
        "Mark CDS form",
        "Return to Main Menu",
    ]

    while True:
        selection: int = interact(menu)
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match int(selection):
            case 1:
                ds.raise_for_status()
                # request_cds_form(app_ds, history)
                request_cds_form(ds, history)
                print("Generated CDS Form Successfully\n")
            case 2:
                # app_ds = load()
                cds_form_stream, info = retrieve_cds_form(history)
                if cds_form_stream is not None:
                    # app_ds = record_cds(app_ds, cds_form_stream)
                    record_cds(ds, cds_form_stream)
                    history.add_recorded_cds_form(info)
                    save_retrieve(info)
                    print("Marked CDS Records")
            case _:
                break

        # save(app_ds)
        save(ds)
        history.save()

    return None

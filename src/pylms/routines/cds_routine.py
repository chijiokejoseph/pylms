import pandas as pd

from pylms.state import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import load, save
from pylms.forms.request_form_api import (
    request_cds_form,
)
from pylms.forms.retrieve_form_api import (
    RetrieveType,
    retrieve_cds_form,
    save_retrieve,
)
from pylms.rollcall import (
    cds,
)
from pylms.utils import DataStream


def handle_cds() -> None:
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
                app_ds = load()
                request_cds_form(app_ds)
                print("Generated CDS Form Successfully\n")
            case 2:
                app_ds = load()
                cds_form_stream: DataStream[pd.DataFrame] | None = retrieve_cds_form()
                if cds_form_stream is not None:
                    app_ds = cds(app_ds, cds_form_stream)
                    save_retrieve(RetrieveType.CDS)
                    print("Marked CDS Records")
            case _:
                break

        save(app_ds)

    return None

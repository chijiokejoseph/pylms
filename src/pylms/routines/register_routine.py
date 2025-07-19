from pylms.state import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import append_update, load, new, save
from pylms.forms.request_form_api import (
    request_update_form,
)
from pylms.forms.retrieve_form_api import (
    retrieve_update_form,
    save_retrieve,
)
from pylms.rollcall import (
    GlobalRecord,
    extract_cds,
    record_cds,
)
from pylms.state import History
from pylms.utils import DataStore


def register() -> None:
    menu: list[str] = [
        "Register New Cohort Data",
        "Request Update Form",
        "Update Cohort Data",
        "Return to Main Menu",
    ]

    history: History = History.load()
    while True:
        selection: int = interact(menu)
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)
        match int(selection):
            case 1:
                app_ds: DataStore = new()
                print("Onboarding of Registered Students completed successfully.\n")
            case 2:
                app_ds = load()
                request_update_form(app_ds)
                print("Generated Data Form successfully\n")
            case 3:
                global_record: GlobalRecord = GlobalRecord()
                app_ds = load()
                data_form_stream, info = retrieve_update_form(history)
                if data_form_stream is not None:
                    data_form_stream, cds_data_stream = extract_cds(data_form_stream)
                    app_ds = append_update(app_ds, data_form_stream)
                    app_ds = record_cds(app_ds, cds_data_stream)
                    app_ds = global_record.crosscheck(app_ds)
                    save_retrieve(info)
                    print("CDS data marked successfully\n")
                else:
                    print(
                        "Couldn't mark CDS data. See the earlier prints for the reasons.\n"
                    )
            case _:
                break

        save(app_ds)
        history.save()

    return None

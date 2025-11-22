import pandas as pd

from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import append_update, new, save
from pylms.errors import Result, eprint
from pylms.forms.request_form_api import request_unregistered_form, request_update_form
from pylms.forms.retrieve_form_api import (
    retrieve_update_form,
    save_retrieve,
)
from pylms.history import History
from pylms.info import printpass
from pylms.models.form_info import UpdateFormInfo
from pylms.rollcall import (
    GlobalRecord,
    extract_cds,
    record_cds,
)
from pylms.utils import DataStore
from pylms.utils.data.datastream import DataStream


def register(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Register New Cohort Data",
        "Request Update Form",
        "Retrieve Update Form and Update Cohort Data",
        "Request Unregistered Form",
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
                app_ds_result = new(history)
                if app_ds_result.is_err():
                    continue
                app_ds: DataStore = app_ds_result.unwrap()
                ds.copy_from(app_ds)
                printpass("Onboarding of Registered Students completed successfully.\n")
            case 2:
                request_update_form(ds, history)
                printpass("Generated Update Form successfully\n")
            case 3:
                global_record: GlobalRecord = GlobalRecord()
                result: Result[
                    tuple[DataStream[pd.DataFrame] | None, UpdateFormInfo]
                ] = retrieve_update_form(history)
                if result.is_err():
                    eprint(
                        f"\nFailed to retrieve update form with error: {result.unwrap_err()}\n"
                    )
                    continue
                data_form_stream, info = result.unwrap()
                if data_form_stream is not None:
                    data_form_stream, cds_data_stream = extract_cds(data_form_stream)
                    append_update(ds, data_form_stream, info)
                    record_cds(ds, cds_data_stream)
                    global_record.crosscheck(ds)
                    save_retrieve(info)
                    history.add_recorded_update_form(info)
                    printpass("CDS data marked successfully\n")
                else:
                    eprint(
                        "Couldn't mark CDS data. See the earlier prints for the reasons.\n"
                    )
            case 4:
                request_unregistered_form(ds)
            case _:
                break

        save(ds)
        history.save()

    return None

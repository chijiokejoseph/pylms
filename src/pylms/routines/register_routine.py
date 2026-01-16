from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import append_update, new, save
from ..form_request import request_complaint_form, request_update_form
from ..form_retrieve import (
    retrieve_update_form,
)
from ..history import History, add_recorded_update_form, save_history
from ..info import print_info, printpass
from ..rollcall import (
    extract_cds,
    record_cds,
)


def register(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Register New Cohort Data",
        "Request Update Form",
        "Retrieve Update Form and Update Cohort Data",
        "Request Complaint Form",
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
                app_ds = new(history)
                if app_ds.is_err():
                    continue
                app_ds = app_ds.unwrap()
                ds.copy_from(app_ds)
                printpass("Onboarding of Registered Students completed successfully.\n")
            case 2:
                result = request_update_form(ds, history)
                if result.is_err():
                    continue
                printpass("Generated Update Form successfully\n")
            case 3:
                result = retrieve_update_form(history)

                if result.is_err():
                    continue

                data_stream, info = result.unwrap()
                data_stream, cds_data_stream = extract_cds(data_stream)

                result = append_update(ds, data_stream, info)
                if result.is_err():
                    continue

                record_cds(ds, cds_data_stream)
                add_recorded_update_form(history, info)
                printpass("CDS data marked successfully\n")
            case 4:
                result = request_complaint_form(ds)
                if result.is_err():
                    continue

                printpass("Generated complaint form successfully")
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

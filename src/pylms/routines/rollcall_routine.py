from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import save
from ..form_request import request_class_form
from ..history import (
    History,
    save_history,
)
from ..info import print_info, printpass
from ..rollcall import (
    record_cohort,
    run_record,
)
from ..rollcall_edit import (
    edit_record,
)


def handle_rollcall(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Request Attendance for a class",
        "Mark Attendance for a class",
        "Edit Student Attendance Manually",
        "Record Current Cohort Attendance",
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
                result = request_class_form(ds, history)
                if result.is_err():
                    continue

                printpass("Generated Attendance Form successfully\n")
            case 2:
                result = run_record(ds, history)
                if result.is_err():
                    continue

            case 3:
                edit_result = edit_record(ds, history)

                if edit_result.is_err():
                    continue
            case 4:
                record_path = record_cohort(ds, history)
                if record_path.is_err():
                    continue

                record_path = record_path.unwrap()
                printpass(
                    f"Generated half cohort data successfully.\nPath: '{record_path.resolve()}'\n"
                )
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

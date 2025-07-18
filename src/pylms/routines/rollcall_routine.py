import pandas as pd

from pylms.state import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import load, save
from pylms.forms.request_form_api import (
    request_class_form,
)
from pylms.forms.retrieve_form_api import (
    ClassType,
    RetrieveType,
    retrieve_class_form,
    save_retrieve,
)
from pylms.rollcall import (
    EditType,
    input_class_date,
    input_date_for_edit,
    record_absent,
    record_excused,
    record_mid_cohort,
    edit_record,
    record_present,
)
from pylms.utils import DataStream


def handle_rollcall() -> None:
    menu: list[str] = [
        "Request Attendance for a class",
        "Mark Attendance for a class",
        "Edit Student Attendance Manually",
        "Record Half Cohort Attendance",
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
                request_class_form(app_ds)
                print("Generated Attendance Form successfully\n")
            case 2:
                app_ds = load()
                class_dates: list[str] = input_class_date()
                for each_date in class_dates:
                    present_turnout: DataStream[pd.DataFrame] | None = (
                        retrieve_class_form(each_date, ClassType.PRESENT)
                    )
                    excused_turnout: DataStream[pd.DataFrame] | None = (
                        retrieve_class_form(each_date, ClassType.EXCUSED)
                    )
                    if present_turnout is None or excused_turnout is None:
                        continue

                    if not present_turnout.is_empty():
                        app_ds = record_present(app_ds, present_turnout)
                        print(f"Attendance for {each_date} marked successfully")
                    else:
                        print(
                            f"Class Form for {each_date} which marks 'Present' students has no responses"
                        )

                    if not excused_turnout.is_empty():
                        app_ds = record_excused(app_ds, excused_turnout)
                        print(f"Excused List for {each_date} marked successfully")
                    else:
                        print(
                            f"Class Form for {each_date} which marks 'Excused' students has no responses"
                        )

                    app_ds = record_absent(app_ds, present_turnout)
                    save_retrieve(RetrieveType.CLASS, each_date)
                    print(f"Recorded all those absent for date '{each_date}'")
                    print()
            case 3:
                app_ds = load()
                input_dates: list[str] = input_date_for_edit()
                app_ds, batch_type = edit_record(app_ds, input_dates)
                # only save retrieval if the record attendance manually was done for the whole batch of Students
                if batch_type == EditType.ALL:
                    for each_date in input_dates:
                        save_retrieve(RetrieveType.CLASS, each_date)
            case 4:
                app_ds = load()
                record_path = record_mid_cohort(app_ds)
                if record_path is not None:
                    print(
                        f"Generated half cohort data successfully at path '{record_path.resolve()}'\n"
                    )
                else:
                    print("Could not generate half cohort data\n")
            case _:
                break

        save(app_ds)
    return None

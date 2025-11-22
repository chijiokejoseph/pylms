import pandas as pd

from pylms.cache import cache_for_cmd
from pylms.cli import interact
from pylms.data_ops import save
from pylms.forms.request_form_api import (
    request_class_form,
)
from pylms.forms.retrieve_form_api import (
    ClassType,
    retrieve_class_form,
    save_retrieve,
)
from pylms.history import History
from pylms.info import println, printpass
from pylms.rollcall import (
    EditType,
    edit_record,
    input_class_date,
    new_edit_info,
    record_absent,
    record_cohort,
    record_excused,
    record_present,
)
from pylms.utils import DataStore, DataStream


def handle_rollcall(ds: DataStore, history: History) -> None:
    menu: list[str] = [
        "Request Attendance for a class",
        "Mark Attendance for a class",
        "Edit Student Attendance Manually",
        "Record Current Cohort Attendance",
        "Return to Main Menu",
    ]

    while True:
        selection_result = interact(menu)
        if selection_result.is_err():
            print(f"Error retrieving selection: {selection_result.unwrap_err()}")
            continue
        selection: int = selection_result.unwrap()
        cmd: str = menu[selection - 1]
        if selection < len(menu):
            cache_for_cmd(cmd)

        match selection:
            case 1:
                request_class_form(ds, history)
                printpass("Generated Attendance Form successfully\n")
            case 2:
                dates_result = input_class_date(history)
                if dates_result.is_err():
                    continue
                class_dates = dates_result.unwrap()

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
                        record_present(ds, present_turnout)
                        println(f"Attendance for {each_date} marked successfully")
                    else:
                        println(
                            f"Class Form for {each_date} which marks 'Present' students has no responses"
                        )

                    if not excused_turnout.is_empty():
                        record_excused(ds, excused_turnout)
                        println(f"Excused List for {each_date} marked successfully")
                    else:
                        println(
                            f"Class Form for {each_date} which marks 'Excused' students has no responses"
                        )

                    record_absent(ds, present_turnout, each_date)
                    info = history.match_info_by_date(each_date)
                    save_retrieve(info)
                    history.add_recorded_class_form(info)
                    history.add_marked_class(class_date=each_date)
                    printpass(f"Recorded all those absent for date '{each_date}'")
                    print()
            case 3:
                edit_result = edit_record(ds, history)
                if edit_result.is_err():
                    continue
                edit_type, edited_dates = edit_result.unwrap()

                # only save retrieval if the record attendance manually was done for the whole batch of Students
                if edit_type == EditType.ALL:
                    for each_date in edited_dates:
                        history.add_marked_class(class_date=each_date)
                        save_retrieve(new_edit_info(each_date))
            case 4:
                record_path = record_cohort(ds, history)
                if record_path is not None:
                    println(
                        f"Generated half cohort data successfully at path '{record_path.resolve()}'\n"
                    )
                else:
                    print("Could not generate half cohort data\n")
            case _:
                break

        save(ds)
        history.save()
    return None

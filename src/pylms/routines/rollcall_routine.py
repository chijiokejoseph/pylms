from ..cache import cache_for_cmd
from ..cli import interact
from ..data import DataStore
from ..data_service import save
from ..errors import eprint
from ..form_request import request_class_form
from ..form_retrieve import (
    ClassType,
    retrieve_class_form,
    save_retrieve,
)
from ..history import (
    History,
    add_marked_class,
    add_recorded_class_form,
    all_dates,
    get_marked_classes,
    match_info_by_date,
    save_history,
)
from ..info import print_info, printpass
from ..rollcall import (
    input_class_date,
    record_absent,
    record_cohort,
    record_excused,
    record_present,
)
from ..rollcall_edit import (
    EditType,
    edit_record,
    new_edit_info,
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
                dates_result = input_class_date(history)

                if dates_result.is_err():
                    continue

                class_dates = dates_result.unwrap()

                for each_date in class_dates:
                    present_turnout = retrieve_class_form(each_date, ClassType.PRESENT)

                    if present_turnout.is_err():
                        continue

                    present_turnout = present_turnout.unwrap()

                    excused_turnout = retrieve_class_form(each_date, ClassType.EXCUSED)

                    if excused_turnout.is_err():
                        continue

                    excused_turnout = excused_turnout.unwrap()

                    if not present_turnout.is_empty():
                        record_present(ds, present_turnout)
                        print_info(f"Attendance for {each_date} marked successfully")
                    else:
                        print_info(
                            f"Class Form for {each_date} which marks 'Present' students has no responses"
                        )

                    if not excused_turnout.is_empty():
                        record_excused(ds, excused_turnout)
                        print_info(f"Excused List for {each_date} marked successfully")
                    else:
                        print_info(
                            f"Class Form for {each_date} which marks 'Excused' students has no responses"
                        )

                    record_absent(ds, present_turnout, each_date)
                    info = match_info_by_date(history, each_date)

                    result = save_retrieve(info)

                    if result.is_err():
                        class_num = all_dates(history, "").index(each_date) + 1
                        eprint(
                            f"Failed to save records for Class {class_num} on '{each_date}'. Please retry for Class {class_num}"
                        )
                        continue

                    _ = result.unwrap()

                    add_recorded_class_form(history, info)
                    _ = add_marked_class(history, each_date).unwrap()
                    print_info(f"Recorded all those absent for date '{each_date}'")

                for date in get_marked_classes(history, ""):
                    class_num = all_dates(history, "").index(date)
                    printpass(
                        f"Recorded attendance for Class {class_num} held on '{date}'"
                    )
            case 3:
                edit_result = edit_record(ds, history)

                if edit_result.is_err():
                    continue

                edit_type, edited_dates = edit_result.unwrap()

                marked_dates: list[str] = []

                # only save retrieval if the record attendance manually was done for the whole batch of Students
                if edit_type == EditType.ALL:
                    for each_date in edited_dates:
                        result = add_marked_class(history, each_date)
                        if result.is_err():
                            continue
                        result = save_retrieve(new_edit_info(each_date))
                        if result.is_err():
                            continue

                        marked_dates.append(each_date)

                    for date in marked_dates:
                        class_num = all_dates(history, "").index(date)
                        printpass(
                            f"Recorded attendance for Class {class_num} held on '{date}'"
                        )
            case 4:
                record_path = record_cohort(ds, history)
                if record_path.is_err():
                    continue

                record_path = record_path.unwrap()
                printpass(
                    f"Generated half cohort data successfully at path '{record_path.resolve()}'\n"
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

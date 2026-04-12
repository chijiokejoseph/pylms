from pylms.cli import input_bool
from pylms.constants import COMMA_DELIM
from pylms.query_dates import search_unmarked
from ..data import DataStore
from ..errors import ForcedExitError, Result, Unit, eprint
from ..form_retrieve import ClassType, retrieve_class_form
from ..history import (
    History,
    add_marked_class,
    add_recorded_class_form,
    get_class_info,
    get_date_index,
)
from ..info import print_info, printpass
from .absent import record_absent
from .excused import record_excused
from .present import record_present


def run_record(ds: DataStore, history: History) -> Result[Unit]:
    """Record attendance for selected class dates.

    Args:
        ds (DataStore): DataStore containing student data.
        history (History): History object for tracking operations.

    Returns:
        Result[Unit]: Success or error message.
    """
    while True:
        dates = search_unmarked(history)

        if dates.is_err():
            return dates.propagate()

        dates = dates.unwrap()
        print_info(f"Selected Dates are [{COMMA_DELIM.join(dates)}]")
        choice = input_bool("Confirm selected dates?")
        if choice.is_err() and isinstance(choice.error, ForcedExitError):
            return choice.propagate()
        elif choice.is_err():
            continue
        
        if not choice.unwrap():
            eprint("You rejected selected dates")
            return choice.propagate()
        
        break

    # Process each selected date
    for each_date in dates:
        # Retrieve present and excused student forms
        present_turnout = retrieve_class_form(history, each_date, ClassType.PRESENT)

        if present_turnout.is_err():
            continue

        present_turnout = present_turnout.unwrap()

        excused_turnout = retrieve_class_form(history, each_date, ClassType.EXCUSED)

        if excused_turnout.is_err():
            continue

        excused_turnout = excused_turnout.unwrap()

        # Record present students
        if not present_turnout.is_empty():
            result = record_present(ds, present_turnout)
            if result.is_err():
                continue

            print_info(f"Attendance for {each_date} marked successfully")
        else:
            print_info(
                f"Class Form for {each_date} which marks 'Present' students has no responses"
            )

        # Record excused students
        if not excused_turnout.is_empty():
            result = record_excused(ds, excused_turnout)
            if result.is_err():
                continue

            print_info(f"Excused List for {each_date} marked successfully")
        else:
            print_info(
                f"Class Form for {each_date} which marks 'Excused' students has no responses"
            )

        # Record absent students
        result = record_absent(ds, each_date)
        if result.is_err():
            continue

        # Update history with recorded form info
        info = get_class_info(history, each_date)
        if info.is_err():
            continue
        info = info.unwrap()

        add_recorded_class_form(history, info)
        _ = add_marked_class(history, each_date).unwrap()
        print_info(f"Recorded all those absent for date '{each_date}'")

    # Print summary of recorded attendance
    for date in dates:
        class_num = get_date_index(history, date).unwrap()
        printpass(f"Recorded attendance for Class {class_num} held on '{date}'")

    return Result.unit()

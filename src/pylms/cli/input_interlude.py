from datetime import datetime, timedelta

from ..constants import COMMA_DELIM, DATE_FMT, WEEK_DAYS
from ..errors import ForcedExitError, Result, eprint
from ..history import History, Interlude, all_dates
from .classes_input import select_class_date
from .custom_inputs import input_num, input_str
from .option_input import input_option


def _test_end_datetime(history: History, end: datetime) -> bool:
    weekday = end.weekday()
    days = history.class_days

    if weekday not in days:
        days = [WEEK_DAYS[day] for day in days]
        printout = COMMA_DELIM.join(days)
        resume_day = WEEK_DAYS[weekday]

        msg = f"Your classes hold on {printout}, but your specified resumption day is {resume_day}"
        eprint(msg)
        return False

    return True


def get_interlude_dates(history: History) -> Result[Interlude]:
    dates = all_dates(history, "")

    class_date: str

    while True:
        selected = select_class_date(
            "Select the Class Date when the Interlude starts", dates
        )
        if selected.is_err():
            return selected.propagate()
        selected = selected.unwrap()

        if len(selected) > 1:
            selection = ", ".join(selected)
            msg = f"Only a single class date should be selected but multiple dates have been selected: '{selection}'"
            eprint(msg)
            continue

        class_date = selected[0]
        break

    start = datetime.strptime(class_date, DATE_FMT)

    menu = ["Enter resumption date", "Enter days shift"]
    choice = input_option(
        menu, "Interlude Menu", "Select how you intend to specify the interlude"
    )
    if choice.is_err():
        return choice.propagate()
    idx, _ = choice.unwrap()

    if idx == 2:
        while True:
            days_shift = input_num("Enter the interlude days: ", 0)

            if days_shift.is_err() and isinstance(days_shift.error, ForcedExitError):
                return days_shift.propagate()
            elif days_shift.is_err():
                continue

            days_shift = days_shift.unwrap()

            end = start + timedelta(days=days_shift)

            if not _test_end_datetime(history, end):
                continue

            interlude = Interlude.new(start, days_shift)
            if interlude.is_err():
                continue

            interlude = interlude.unwrap()
            return Result.ok(interlude)

    while True:
        resume_date = input_str(
            "Enter the resumption class day in the format dd/mm/yyyy"
        )
        if resume_date.is_err():
            return resume_date.propagate()
        resume_date = resume_date.unwrap()

        try:
            resume_date = datetime.strptime(resume_date, DATE_FMT)
        except Exception:
            msg = f"Failed to parse resumption date: '{resume_date} in date format {DATE_FMT}"
            eprint(msg)
            continue

        if not _test_end_datetime(history, resume_date):
            continue

        interlude = Interlude.new(start, resume_date)
        if interlude.is_err():
            continue

        return interlude

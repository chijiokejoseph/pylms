import re
from datetime import datetime, timedelta

from pylms.constants import DATE, DATE_FMT
from pylms.utils.data import DataStore
from pylms.utils.date.errors import CaseUnreachableError, DateCourseMismatchError


def _det_dates(ds: DataStore, num_weeks: int) -> list[str]:
    from pylms.cli import input_str

    msg: str = """
Marking the dates for which classes will hold
Please enter the start date for the classes.
Enter the date in the format dd/mm/yyyy: """
    cohort_date_str: str = ds()[DATE].iloc[0]
    cohort_date: datetime = datetime.strptime(cohort_date_str, DATE_FMT)
    bad_pattern_msg: str = (
        "Your input does not match the specified pattern of dd/mm/yyyy."
    )
    invalid_date_msg: str = f"Entered date is behind {cohort_date_str}, the orientation date of the cohort. How is that possible?"
    diagnosis_map: dict[str, str] = {"result": ""}

    def validator(str_input: str) -> bool:
        pattern: re.Pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
        matches: re.Match | None = pattern.match(str_input)
        if matches is None:
            diagnosis_map["result"] = bad_pattern_msg
            return False
        start_input: datetime = datetime.strptime(str_input, DATE_FMT)
        if start_input < cohort_date:
            diagnosis_map["result"] = invalid_date_msg
            return False
        return True

    start_date_str: str = input_str(msg, validator, diagnosis=diagnosis_map["result"])
    start_date: datetime = datetime.strptime(start_date_str, DATE_FMT)

    # 0 - 6 (Mon - Sun)
    # weekday_start is expected to range from 0 to 2
    # since Python Beginners Classes are from Mon - Wed
    weekday_start: int = start_date.weekday()
    if weekday_start > 2:
        raise DateCourseMismatchError(
            "Forcefully exiting since the entered start date does not conform to the schedule for Python Beginners. \nAn edit to the program is likely required to remove this feature. \nIf this is a mistake, please restart the program and enter a date that lies between Monday to Wednesday."
        )
    num_weekly_classes: int = 3
    rem_first_weekdays: int = num_weekly_classes - weekday_start
    days_range = range(rem_first_weekdays)
    first_week: list[datetime] = [start_date + timedelta(days=i) for i in days_range]

    match int(weekday_start):
        case 0:
            next_week_start: datetime = start_date + timedelta(days=7)
        case 1:
            next_week_start = start_date + timedelta(days=6)
        case 2:
            next_week_start = start_date + timedelta(days=5)
        case _:
            raise CaseUnreachableError("You shouldn't be here")

    rem_weeks: int = num_weeks - 1
    rem_days: list[int] = [i for i in range(rem_weeks * 7) if i % 7 < 3]
    other_weeks: list[datetime] = [
        next_week_start + timedelta(days=i) for i in rem_days
    ]
    classes: list[datetime] = first_week.copy()
    classes.extend(other_weeks)
    return [value.strftime(DATE_FMT) for value in classes]

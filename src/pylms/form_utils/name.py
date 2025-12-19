from datetime import datetime
from typing import NamedTuple

from ..constants import DATE_FMT, FORM_DATE_FMT, TIMESTAMP_FMT


class FormHead(NamedTuple):
    title: str
    name: str


def return_name(cohort: int, function: str, date: str | None = None) -> FormHead:
    if date is None:
        timestamp = datetime.now().strftime(TIMESTAMP_FMT)
        form_title: str = f"Python Beginners Cohort {cohort} {function}"
        form_name: str = f"Cohort {cohort} {function} {timestamp}"
    else:
        name_date = datetime.strptime(date, DATE_FMT).strftime(FORM_DATE_FMT)
        form_title = f"Python Beginners Cohort {cohort} {function} for {date}"
        form_name = f"Cohort {cohort} {function} {name_date}"

    return FormHead(title=form_title, name=form_name)

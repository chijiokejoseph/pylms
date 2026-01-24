from datetime import datetime
from typing import NamedTuple

from ..constants import DATE_FMT, FORM_DATE_FMT, TIMESTAMP_FMT


class FormHead(NamedTuple):
    """Named tuple for form title and name."""
    title: str
    name: str


def return_name(cohort: int, function: str, date: str | None = None) -> FormHead:
    """Generate form title and name based on cohort, function, and optional date.
    
    Args:
        cohort (int): Cohort number.
        function (str): Form function/purpose (e.g., 'Attendance', 'CDS').
        date (str | None): Optional date for the form.
        
    Returns:
        FormHead: Named tuple containing formatted title and name.
    """
    if date is None:
        # Generate timestamp-based form name
        timestamp = datetime.now().strftime(TIMESTAMP_FMT)
        form_title: str = f"Python Beginners Cohort {cohort} {function}"
        form_name: str = f"Cohort {cohort} {function} {timestamp}"
    else:
        # Generate date-based form name
        name_date = datetime.strptime(date, DATE_FMT).strftime(FORM_DATE_FMT)
        form_title = f"Python Beginners Cohort {cohort} {function} for {date}"
        form_name = f"Cohort {cohort} {function} {name_date}"

    return FormHead(title=form_title, name=form_name)

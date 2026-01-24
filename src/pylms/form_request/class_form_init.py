from datetime import datetime

from ..cli import input_email
from ..constants import TIMESTAMP_FMT
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History, add_class_form, add_held_class
from ..models import ClassFormInfo
from .excused_class_form import init_excused_form
from .present_class_form import init_present_form


def init_class_form(
    ds: DataStore, history: History, form_dates: list[str]
) -> Result[Unit]:
    """Initialize class forms for attendance tracking on specified dates.
    
    Creates both present and excused forms for each date, then adds the form
    information to history and marks classes as held.
    
    Args:
        ds (DataStore): DataStore containing student data.
        history (History): History object for tracking operations.
        form_dates (list[str]): List of dates to create forms for.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    email = input_email(
        "Enter an email address to share the form with: ",
    )
    if email.is_err():
        return email.propagate()
    email = email.unwrap()

    # Create forms for each specified date
    for date in form_dates:
        # Create present form
        present_form = init_present_form(ds, date, email)
        if present_form.is_err():
            return present_form.propagate()
        present_form = present_form.unwrap()

        # Create excused form
        excused_form = init_excused_form(ds, date, email)
        if excused_form.is_err():
            return excused_form.propagate()
        excused_form = excused_form.unwrap()

        # Create form info record
        form_info: ClassFormInfo = ClassFormInfo(
            date=date,
            present_name=present_form.name,
            present_title=present_form.title,
            present_url=present_form.url,
            present_id=present_form.uuid,
            excused_name=excused_form.name,
            excused_title=excused_form.title,
            excused_url=excused_form.url,
            excused_id=excused_form.uuid,
            timestamp=datetime.now().strftime(TIMESTAMP_FMT),
        )
        
        # Update history with held class and form info
        result = add_held_class(history, date)
        if result.is_err():
            return result.propagate()

        add_class_form(history, form_info)

    return Result.unit()

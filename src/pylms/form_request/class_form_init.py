from datetime import datetime

from ..config import Config
from ..constants import TIMESTAMP_FMT
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History, add_class_form, add_held_class
from ..models import ClassFormInfo
from .excused_class_form import init_excused_form
from .present_class_form import init_present_form
from .share_emails import input_share_emails


def init_class_form(
    config: Config, ds: DataStore, history: History, form_dates: list[str]
) -> Result[Unit]:
    """Initialize class forms for attendance tracking on specified dates.

    Creates both present and excused forms for each date, shares with admin
    and selected facilitators, then adds the form information to history.

    Args:
        config: Config containing admin and facilitator information.
        ds: DataStore containing student data.
        history: History object for tracking operations.
        form_dates: List of dates to create forms for.

    Returns:
        Result[Unit]: Success or error message.
    """
    # Get emails to share with
    gmails_result = input_share_emails(config)
    if gmails_result.is_err():
        return gmails_result.propagate()
    gmails = gmails_result.unwrap()

    # Create forms for each date
    for date in form_dates:
        present_form = init_present_form(ds, date, gmails)
        if present_form.is_err():
            return present_form.propagate()
        present_form = present_form.unwrap()

        excused_form = init_excused_form(ds, date, gmails)
        if excused_form.is_err():
            return excused_form.propagate()
        excused_form = excused_form.unwrap()

        # Save form info to history
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

        result = add_held_class(history, date)
        if result.is_err():
            return result.propagate()

        add_class_form(history, form_info)

    return Result.unit()

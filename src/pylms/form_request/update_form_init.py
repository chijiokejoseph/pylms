from ..config import Config
from ..data import DataStore
from ..date import to_week_num
from ..errors import Result, Unit
from ..form_utils import (
    UpdateFormDetails,
    extract_update_details,
    new_update_content,
)
from ..history import History, add_update_form
from ..info import print_info
from ..models import (
    ContentBody,
    UpdateFormInfo,
)
from ..query_dates import search_held
from ..service import (
    run_create_form,
    run_setup_form,
    run_share_form_multiple,
)
from .share_emails import input_share_emails


def init_update_form(config: Config, ds: DataStore, history: History) -> Result[Unit]:
    """Initialize update form for students to fill attendance for past dates.

    Creates a form allowing students to update their attendance for held classes
    within the current week number. Shares with admin and selected facilitators.

    Args:
        config: Config containing admin and facilitator information.
        ds: DataStore containing student data.
        history: History object for tracking operations.

    Returns:
        Result[Unit]: Success or error message.
    """
    print_info("""
You'll now select the dates for which the fillers of this form can fill their attendance.
Please select all the dates for which attendance can be filled using the instructions below.
    """)

    dates = search_held(history)

    if dates.is_err():
        return dates.propagate()

    dates = dates.unwrap()

    # Extract form details and filter dates by week number
    result: UpdateFormDetails = extract_update_details(ds)
    form_title: str = result.title
    form_name: str = result.name
    week_num: int = result.week_num
    timestamp: str = result.timestamp

    dates = [each_date for each_date in dates if to_week_num(each_date) <= week_num]
    print_info(
        f"The current week number of the year {result.year_num} is {result.week_num} \nHence, only dates: {dates} which belong to weeks equal to or below {result.week_num} are allowed"
    )

    # Create and setup form
    data_form_result = run_create_form(form_title, form_name)
    if data_form_result.is_err():
        return data_form_result.propagate()
    data_form = data_form_result.unwrap()

    data_form_content: ContentBody = new_update_content(dates)
    
    data_form_result = run_setup_form(data_form, data_form_content)
    if data_form_result.is_err():
        return data_form_result.propagate()
    data_form = data_form_result.unwrap()

    # Share form with admin and selected facilitators
    gmails_result = input_share_emails(config)
    if gmails_result.is_err():
        return gmails_result.propagate()
    gmails = gmails_result.unwrap()

    share_result = run_share_form_multiple(data_form, gmails)
    if share_result.is_err():
        return share_result.propagate()

    # Save form info to history
    info: UpdateFormInfo = UpdateFormInfo(
        week_num=week_num,
        year_num=result.year_num,
        name=data_form.name,
        title=data_form.title,
        dates=dates,
        url=data_form.url,
        uuid=data_form.uuid,
        timestamp=timestamp,
    )
    add_update_form(history, info)
    return Result.unit()

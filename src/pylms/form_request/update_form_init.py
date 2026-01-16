from ..cli import input_email, select_class_date
from ..data import DataStore
from ..date import to_week_num
from ..errors import Result, Unit, eprint
from ..form_utils import (
    UpdateFormDetails,
    extract_update_details,
    new_update_content,
)
from ..history import History, add_update_form, get_held_classes
from ..info import print_info
from ..models import (
    ContentBody,
    Form,
    UpdateFormInfo,
)
from ..service import (
    run_create_form,
    run_setup_form,
    run_share_form,
)


def init_update_form(ds: DataStore, history: History) -> Result[Unit]:
    msg: str = """
You'll now select the dates for which the fillers of this form can fill their attendance.
Please select all the dates for which attendance can be filled using the instructions below.
    """
    dates = get_held_classes(history, "")

    dates = select_class_date(msg, dates)

    if dates.is_err():
        return dates.propagate()

    dates = dates.unwrap()
    result: UpdateFormDetails = extract_update_details(ds)
    form_title: str = result.title
    form_name: str = result.name
    week_num: int = result.week_num
    timestamp: str = result.timestamp

    dates = [each_date for each_date in dates if to_week_num(each_date) <= week_num]
    print_info(
        f"The current week number of the year {result.year_num} is {result.week_num} \nHence, only dates: {dates} which belong to weeks equal to or below {result.week_num} are allowed"
    )
    data_form: Form | None = run_create_form(form_title, form_name)
    if data_form is None:
        msg = "Form creation failed when creating data form. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    data_form_content: ContentBody = new_update_content(dates)
    data_form = run_setup_form(data_form, data_form_content)
    if data_form is None:
        msg = "Form setup failed when setting up data form. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    email = input_email("Enter email to share the form with: ")

    if email.is_err():
        return email.propagate()

    email = email.unwrap()
    data_form = run_share_form(data_form, email)
    if data_form is None:
        msg = f"Form sharing failed when sharing the form. with {email} \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

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

import json
from pathlib import Path

from ..cli import input_email, select_class_date
from ..data import DataStore
from ..date import to_week_num
from ..errors import Result, Unit, eprint
from ..form_utils import (
    UpdateFormDetails,
    extract_update_details,
    new_update_content,
)
from ..history import History, add_update_form
from ..info import print_info
from ..models import (
    ContentBody,
    Form,
    UpdateFormInfo,
)
from ..paths import get_update_path
from ..rollcall import GlobalRecord
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
    global_record = GlobalRecord().new()
    if global_record.is_err():
        return global_record.propagate()

    global_record = global_record.unwrap()
    src_dates = global_record.retrieve_unset_dates()

    dates_result = select_class_date(msg, src_dates)

    if dates_result.is_err():
        return dates_result.propagate()

    dates_list: list[str] = dates_result.unwrap()
    result: UpdateFormDetails = extract_update_details(ds)
    form_title: str = result.title
    form_name: str = result.name
    week_num: int = result.week_num
    timestamp: str = result.timestamp

    dates_list = [
        each_date for each_date in dates_list if to_week_num(each_date) <= week_num
    ]
    print_info(
        f"The current week number of the year {result.year_num} is {result.week_num} \nHence, only dates: {dates_list} which belong to weeks equal to or below {result.week_num} are allowed"
    )
    data_form: Form | None = run_create_form(form_title, form_name)
    if data_form is None:
        msg = "Form creation failed when creating data form. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    data_form_content: ContentBody = new_update_content(dates_list)
    data_form = run_setup_form(data_form, data_form_content)
    if data_form is None:
        msg = "Form setup failed when setting up data form. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    email_result = input_email("Enter email to share the form with: ")

    if email_result.is_err():
        return email_result.propagate()

    recipient_email: str = email_result.unwrap()
    data_form = run_share_form(data_form, recipient_email)
    if data_form is None:
        msg = f"Form sharing failed when sharing the form. with {recipient_email} \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    info: UpdateFormInfo = UpdateFormInfo(
        week_num=week_num,
        year_num=result.year_num,
        name=data_form.name,
        title=data_form.title,
        dates=dates_list,
        url=data_form.url,
        uuid=data_form.uuid,
        timestamp=timestamp,
    )
    add_update_form(history, info)
    update_form_path: Path = get_update_path("form", info.timestamp)
    with open(update_form_path, "w") as json_file:
        json.dump(info.model_dump(), json_file, indent=2)
    return Result.unit()

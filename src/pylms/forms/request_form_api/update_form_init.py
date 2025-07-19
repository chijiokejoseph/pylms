import json
from io import TextIOWrapper
from pathlib import Path
from datetime import datetime
from typing import cast

from pylms.cli import input_email, select_class_date
from pylms.forms.request_form_api.errors import FormServiceError
from pylms.forms.request_form_api.utils import (
    UpdateFormDetails,
    UpdateFormInfo,
    new_content_body,
    scrape_update_form,
)
from pylms.forms.utils.service import (
    create_form,
    setup_form,
    share_form,
)
from pylms.models import (
    ContentBody,
    Form,
)
from pylms.utils import DataStore, date, paths
from pylms.constants import TIMESTAMP_FMT

def init_update_form(ds: DataStore) -> None:
    msg: str = """
You'll now select the dates for which the fillers of this form can fill their attendance.
Please select all the dates for which attendance can be filled using the instructions below.    
    """
    dates_list: list[str] = select_class_date(msg)
    result: UpdateFormDetails = scrape_update_form(ds)
    form_title: str = result.title
    form_name: str = result.name
    week_num: int = result.week_num

    dates_list = [
        each_date for each_date in dates_list if date.to_week_num(each_date) <= week_num
    ]
    print(
        f"The current week number of the year {result.year_num} is {result.week_num} \nHence, only dates: {dates_list} which belong to weeks equal to or below {result.week_num} are allowed"
    )
    data_form: Form | None = create_form(form_title, form_name)
    if data_form is None:
        raise FormServiceError(
            "create",
            "Form creation failed when creating data form. \nPlease restart the program and try again.",
        )

    data_form_content: ContentBody = new_content_body(dates_list)
    data_form = setup_form(data_form, data_form_content)
    if data_form is None:
        raise FormServiceError(
            "setup",
            "Form setup failed when setting up data form. \nPlease restart the program and try again.",
        )

    recipient_email: str = input_email("Enter email to share the form with: ")
    data_form = share_form(data_form, recipient_email)
    if data_form is None:
        raise FormServiceError(
            "share",
            f"Form sharing failed when sharing the form. with {recipient_email} \nPlease restart the program and try again.",
        )

    info: UpdateFormInfo = UpdateFormInfo(
        week_num=week_num,
        year_num=result.year_num,
        name=data_form.name,
        title=data_form.title,
        dates=dates_list,
        url=data_form.url,
        uuid=data_form.uuid,
        timestamp=datetime.now().strftime(TIMESTAMP_FMT)
    )
    update_form_path: Path = paths.get_update_path("form", info.uuid)
    with open(update_form_path, "w") as json_file:
        json.dump(info.model_dump(), cast(TextIOWrapper, json_file), indent=2)

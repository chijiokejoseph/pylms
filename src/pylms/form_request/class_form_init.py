import json
from datetime import datetime

from ..cli import input_email
from ..constants import TIMESTAMP_FMT
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History, add_class_form, add_held_class
from ..models import ClassFormInfo
from ..paths_class import get_class_path
from .excused_class_form import init_excused_form
from .present_class_form import init_present_form


def init_class_form(
    ds: DataStore, history: History, form_dates: list[str]
) -> Result[Unit]:
    email_result = input_email(
        "Enter an email address to share the form with: ",
    )
    if email_result.is_err():
        return email_result.propagate()
    recipient_email: str = email_result.unwrap()

    for date in form_dates:
        metadata_path = get_class_path(date, "class")
        if metadata_path.is_err():
            return metadata_path.propagate()

        metadata_path = metadata_path.unwrap()

        present_form = init_present_form(ds, date, recipient_email)
        if present_form.is_err():
            return present_form.propagate()
        present_form = present_form.unwrap()

        excused_form = init_excused_form(ds, date, recipient_email)
        if excused_form.is_err():
            return excused_form.propagate()
        excused_form = excused_form.unwrap()

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
        with metadata_path.open("w", encoding="utf-8") as file:
            json.dump(form_info.model_dump(), file, indent=2)

    return Result.unit()

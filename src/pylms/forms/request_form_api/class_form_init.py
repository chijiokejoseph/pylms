import json
from io import TextIOWrapper
from pathlib import Path
from typing import cast
from datetime import datetime

from pylms.cli import input_email
from pylms.constants import TIMESTAMP_FMT
from pylms.forms.request_form_api.excused_class_form import init_excused_form
from pylms.forms.request_form_api.present_class_form import init_present_form
from pylms.forms.request_form_api.utils import ClassFormInfo
from pylms.models import Form
from pylms.utils import DataStore, paths
from pylms.history import History


def init_class_form(ds: DataStore, history: History, form_dates: list[str]) -> None:
    recipient_email: str = input_email(
        "Enter an email address to share the form with: ",
    )

    for date in form_dates:
        metadata_path: Path = paths.get_class_path(date, "class")
        present_form: Form = init_present_form(ds, date, recipient_email)
        excused_form: Form = init_excused_form(ds, date, recipient_email)
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
        history.add_held_class(class_date=date)
        history.add_class_form(form_info)
        with metadata_path.open("w", encoding="utf-8") as file:
            json.dump(form_info.model_dump(), cast(TextIOWrapper, file), indent=2)

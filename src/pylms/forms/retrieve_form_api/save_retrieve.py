import json
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import Type, cast

from pydantic import BaseModel

from pylms.constants import FORM_DATE_FMT
from pylms.forms.request_form_api import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from pylms.forms.retrieve_form_api.enums import RetrieveType
from pylms.forms.retrieve_form_api.errors import InvalidRetrieveArgsError
from pylms.utils import date, paths


def save_retrieve(retrieve_type: RetrieveType, class_date: str | None = None) -> None:
    if retrieve_type == RetrieveType.CLASS and class_date is None:
        raise InvalidRetrieveArgsError(
            "You cannot specify retrieve_type as being a class and set `class_date` to None."
        )

    if retrieve_type == RetrieveType.CLASS and class_date is not None:
        form_path: Path = paths.get_class_path(class_date, "class")
        record_path: Path = paths.get_class_path(class_date, "record")
        cls: Type = ClassFormInfo
        if not form_path.exists():
            form_date: str = date.format_date(class_date, FORM_DATE_FMT)
            class_info: ClassFormInfo = ClassFormInfo(
                date=class_date,
                present_name=f"Manual Attendance {form_date}",
                present_id=f"{datetime.now()}",
                present_title="",
                present_url="",
                excused_name=f"Manual Excused List {form_date}",
                excused_id=f"{datetime.now()}",
                excused_title="",
                excused_url="",
            )
            with form_path.open("w", encoding="utf-8") as json_form:
                json.dump(
                    class_info.model_dump(), cast(TextIOWrapper, json_form), indent=2
                )

    elif retrieve_type == RetrieveType.CDS:
        form_path = paths.get_cds_path("form")
        record_path = paths.get_cds_path("record")
        cls = CDSFormInfo
    else:
        form_path, record_path = paths.ret_update_path()
        cls = UpdateFormInfo

    with record_path.open("w", encoding="utf-8") as json_record:
        with form_path.open("r", encoding="utf-8") as json_form:
            data: dict = json.load(json_form)
            data_form_info: BaseModel = cls(**data)
        json.dump(
            data_form_info.model_dump(), cast(TextIOWrapper, json_record), indent=2
        )

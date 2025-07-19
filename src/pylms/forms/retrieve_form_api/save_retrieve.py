import json
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import Type, cast

from pydantic import BaseModel

from pylms.constants import FORM_DATE_FMT, TIMESTAMP_FMT
from pylms.models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from pylms.forms.retrieve_form_api.errors import InvalidRetrieveArgsError
from pylms.utils import date, paths


def _save(form_path: Path, record_path: Path, cls: Type) -> None:
    with record_path.open("w", encoding="utf-8") as json_record:
        with form_path.open("r", encoding="utf-8") as json_form:
            data: dict = json.load(json_form)
            data_form_info: BaseModel = cls(**data)
        json.dump(
            data_form_info.model_dump(), cast(TextIOWrapper, json_record), indent=2
        )

def save_retrieve(info: CDSFormInfo | ClassFormInfo | UpdateFormInfo) -> None:

    match info:
        case _ if isinstance(info, ClassFormInfo):
            form_path: Path = paths.get_class_path(info.date, "class")
            record_path: Path = paths.get_class_path(info.date, "record")
            cls: Type = ClassFormInfo
            if form_path.exists():
                _save(form_path, record_path, cls)
                return

            form_date: str = date.format_date(info.date, FORM_DATE_FMT)
            class_info: ClassFormInfo = ClassFormInfo(
                date=info.date,
                present_name=f"Manual Attendance {form_date}",
                present_id=f"{datetime.now()}",
                present_title="",
                present_url="",
                excused_name=f"Manual Excused List {form_date}",
                excused_id=f"{datetime.now()}",
                excused_title="",
                excused_url="",
                timestamp=datetime.now().strftime(TIMESTAMP_FMT)
            )
            with form_path.open("w", encoding="utf-8") as json_form:
                json.dump(
                    class_info.model_dump(), cast(TextIOWrapper, json_form), indent=2
                )
                
        case _ if isinstance(info, CDSFormInfo):
            form_path = paths.get_cds_path("form", info.uuid)
            record_path = paths.get_cds_path("record", info.uuid)
            cls = CDSFormInfo
        case _ if isinstance(info, UpdateFormInfo):
            form_path, record_path = paths.ret_update_path(info.uuid)
            cls = UpdateFormInfo
        case _:
            raise InvalidRetrieveArgsError("") 
            
    _save(form_path, record_path, cls)
    
    
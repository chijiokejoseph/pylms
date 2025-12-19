import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from ..constants import FORM_DATE_FMT, TIMESTAMP_FMT
from ..date import format_date
from ..errors import Result, Unit, eprint
from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from ..paths import get_cds_path, ret_update_path
from ..paths_class import get_class_path


def _save(form_path: Path, record_path: Path, cls: type) -> None:
    with record_path.open("w", encoding="utf-8") as json_record:
        with form_path.open("r", encoding="utf-8") as json_form:
            data: dict[Any, Any] = json.load(json_form)
            data_form_info: BaseModel = cls(**data)
        json.dump(data_form_info.model_dump(), json_record, indent=2)


def save_retrieve(info: CDSFormInfo | ClassFormInfo | UpdateFormInfo) -> Result[Unit]:
    match info:
        case _ if isinstance(info, ClassFormInfo):
            form_path = get_class_path(info.date, "class")
            if form_path.is_err():
                return form_path.propagate()

            form_path = form_path.unwrap()

            record_path = get_class_path(info.date, "record")
            if record_path.is_err():
                return record_path.propagate()

            record_path = record_path.unwrap()

            cls: type = ClassFormInfo
            if form_path.exists():
                _save(form_path, record_path, cls)
                return Result.unit()

            form_date: str = format_date(info.date, FORM_DATE_FMT)
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
                timestamp=datetime.now().strftime(TIMESTAMP_FMT),
            )
            with form_path.open("w", encoding="utf-8") as json_form:
                json.dump(class_info.model_dump(), json_form, indent=2)

        case _ if isinstance(info, CDSFormInfo):
            form_path = get_cds_path("form", info.timestamp)
            record_path = get_cds_path("record", info.timestamp)
            cls = CDSFormInfo
        case _ if isinstance(info, UpdateFormInfo):
            form_path, record_path = ret_update_path(info.timestamp)
            cls = UpdateFormInfo
        case _:
            msg = f"specified form_info type {type(info).__name__} is invalid"
            eprint(msg)
            return Result.err(msg)

    _save(form_path, record_path, cls)
    return Result.unit()

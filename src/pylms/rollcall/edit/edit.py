from pylms.rollcall.edit.all_records import edit_all_records
from pylms.rollcall.edit.multiple_records import edit_multiple_records
from pylms.rollcall.edit.edit_type import EditType, input_edit_type
from pylms.rollcall.edit.batch_records import edit_batch_records
from pylms.utils import DataStore
from pylms.models import ClassFormInfo
from pylms.constants import TIMESTAMP_FMT
from datetime import datetime


def edit_record(ds: DataStore, dates_to_mark: list[str]) -> tuple[DataStore, EditType]:
    edit_type: EditType = input_edit_type()
    match edit_type:
        case EditType.ALL:
            return edit_all_records(ds, dates_to_mark), edit_type
        case EditType.MULTIPLE:
            return edit_multiple_records(ds, dates_to_mark), edit_type
        case EditType.BATCH:
            return edit_batch_records(ds, dates_to_mark), edit_type


def new_edit_info(class_date: str) -> ClassFormInfo:
    name: str = f"Manual Attendance Entry for {class_date}"
    return ClassFormInfo(
        date=class_date,
        present_name=name,
        present_title=name,
        present_url="",
        present_id="",
        excused_name=name,
        excused_title=name,
        excused_url="",
        excused_id="",
        timestamp=datetime.now().strftime(TIMESTAMP_FMT),
    )

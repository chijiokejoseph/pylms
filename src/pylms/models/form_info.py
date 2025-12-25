from datetime import datetime
from typing import overload

from pydantic import BaseModel

from ..constants import DATE_FMT, TIMESTAMP_FMT


class ClassFormInfo(BaseModel):
    date: str
    present_name: str
    present_title: str
    present_url: str
    present_id: str
    excused_name: str
    excused_title: str
    excused_url: str
    excused_id: str
    timestamp: str


class UpdateFormInfo(BaseModel):
    week_num: int
    year_num: int
    name: str
    title: str
    url: str
    uuid: str
    dates: list[str]
    timestamp: str


class CDSFormInfo(
    BaseModel,
):
    name: str
    title: str
    url: str
    uuid: str
    timestamp: str


@overload
def sort_form(form1: CDSFormInfo) -> int:
    pass


@overload
def sort_form(form1: UpdateFormInfo) -> int:
    pass


@overload
def sort_form(form1: ClassFormInfo) -> int:
    pass


def sort_form(
    form1: CDSFormInfo | UpdateFormInfo | ClassFormInfo,
) -> int:
    if isinstance(form1, CDSFormInfo):
        return datetime.strptime(form1.timestamp, TIMESTAMP_FMT).microsecond
    elif isinstance(form1, UpdateFormInfo):
        return datetime.strptime(form1.timestamp, TIMESTAMP_FMT).microsecond
    else:
        posix = datetime.strptime(form1.date, DATE_FMT).timestamp()
        return int(posix)

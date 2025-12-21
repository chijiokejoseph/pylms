from datetime import datetime

from dateutil.parser import parse

from ..constants import DATE_FMT


def det_week_num() -> int:
    today: datetime = datetime.now()
    return today.isocalendar().week


def to_week_num(date_string: str) -> int:
    date_obj: datetime = datetime.strptime(date_string, DATE_FMT)
    return date_obj.isocalendar().week


def to_week_nums(date_string_list: list[str]) -> list[int]:
    return [to_week_num(date_str) for date_str in date_string_list]


def to_unique_week_nums(date_string_list: list[str]) -> list[int]:
    week_nums: list[int] = list(set(to_week_nums(date_string_list)))
    week_nums.sort()
    return week_nums


def det_year() -> int:
    return datetime.now().year


def to_day_num(entry: str | datetime) -> int:
    if isinstance(entry, str):
        date_obj: datetime = parse(entry, dayfirst=True)
    else:
        date_obj = entry
    return date_obj.isoweekday()

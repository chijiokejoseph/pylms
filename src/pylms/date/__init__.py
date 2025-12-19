from datetime import datetime

from dateutil.parser import parse

from .det_date_features import (
    det_class_num,
    det_week_num,
    det_year,
    to_day_num,
    to_unique_week_nums,
    to_week_num,
    to_week_nums,
)


def format_date(
    date_var: str | datetime, str_format: str, day_first: bool = True
) -> str:
    if isinstance(date_var, str):
        return parse(date_var, dayfirst=day_first).strftime(str_format)
    else:
        return date_var.strftime(str_format)


def format_form_timestamp(date_var: str | datetime, str_format: str) -> str:
    return format_date(date_var, str_format, True)


__all__ = [
    "det_week_num",
    "det_class_num",
    "det_year",
    "to_week_num",
    "to_week_nums",
    "to_unique_week_nums",
    "to_day_num",
    "format_date",
    "format_form_timestamp",
]

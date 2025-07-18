from pathlib import Path

from pylms.rollcall.errors import NoClassFormError
from pylms.utils import paths


def filter_dates(mark_dates: list[str]) -> list[str]:
    valid_mark_dates: list[str] = []
    for each_date in mark_dates:
        date_path: Path = paths.get_class_path(each_date, "class")
        if date_path.exists():
            valid_mark_dates.append(each_date)

    if len(valid_mark_dates) > 0:
        return valid_mark_dates
    else:
        raise NoClassFormError(
            "You have no attendances generated for any of the dates. Please attendance marking is only valid for previously generated attendance forms."
        )

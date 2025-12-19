from ..errors import Result, eprint
from ..paths_class import get_class_path


def filter_dates(mark_dates: list[str]) -> Result[list[str]]:
    valid_mark_dates: list[str] = []
    for each_date in mark_dates:
        date_path = get_class_path(each_date, "class")
        if date_path.is_err():
            return date_path.propagate()

        date_path = date_path.unwrap()

        if date_path.exists():
            valid_mark_dates.append(each_date)

    if len(valid_mark_dates) > 0:
        return Result.ok(valid_mark_dates)
    else:
        msg = "You have no attendances generated for any of the dates. Please attendance marking is only valid for previously generated attendance forms."
        eprint(msg)
        return Result.err(msg)

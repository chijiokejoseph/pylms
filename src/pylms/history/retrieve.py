from datetime import datetime
from typing import Literal, overload

from pylms.errors import Result, eprint

from ..constants import DATE_FMT
from ..date import parse_dates
from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from .history import History


def get_available_class_forms(history: History) -> list[ClassFormInfo]:
    """
    Returns a list of Class Forms that have not been previously retrieved or recorded

    :return: (list[ClassFormInfo]) - A list of Class Forms that are available to retrieve.
    :rtype: list[ClassFormInfo]
    """
    return [
        form for form in history.class_forms if form not in history.recorded_class_forms
    ]


def get_available_cds_forms(history: History) -> list[CDSFormInfo]:
    """
    Returns a list of CDS Forms that have not been previously retrieved or recorded

    :return: (list[CDSFormInfo]) - A list of CDS Forms that are available to retrieve.
    :rtype: list[CDSFormInfo]
    """
    return [
        form for form in history.cds_forms if form not in history.recorded_cds_forms
    ]


def get_available_update_forms(history: History) -> list[UpdateFormInfo]:
    """
    Returns a list of Update Forms that have not been previously retrieved
    or recorded

    :return: (list[UpdateFormInfo]) - A list of Update Forms that are available to retrieve.
    :rtype: list[UpdateFormInfo]
    """
    return [
        form
        for form in history.update_forms
        if form not in history.recorded_update_forms
    ]


def match_info_by_date(history: History, class_date: str) -> Result[ClassFormInfo]:
    """
    Returns a Class Form that matches the given date.

    :param class_date: (str) - The date to match the Class Form to.
    :type class_date: str
    :return: (ClassFormInfo) - The Class Form that matches the given date.
    :rtype: ClassFormInfo
    """
    matched_forms = [form for form in history.class_forms if form.date == class_date]
    if len(matched_forms) == 0:
        msg = f"No class form matches the specified date: {class_date}"
        eprint(msg)
        return Result.err(msg)

    return Result.ok(matched_forms[0])


def get_classes(
    history: History,
    prop: Literal["held", "marked"],
    sample: str | datetime,
    present: bool,
) -> list[str] | list[datetime]:
    if prop == "held":
        dates = history.held_classes
    else:
        dates = history.marked_classes

    if isinstance(sample, datetime):
        if present:
            return dates
        else:
            return [date for date in history.dates if date not in dates]
    else:
        if present:
            return [date.strftime(DATE_FMT) for date in dates]
        else:
            return [
                date.strftime(DATE_FMT) for date in history.dates if date not in dates
            ]


@overload
def get_unheld_classes(history: History, sample: datetime) -> list[datetime]:
    """
    Returns a list of unheld classes i.e., classes that are not part of the held_classes list.

    :return: (list[datetime]) - A list of datetime objects representing the unheld classes.
    :rtype: list[datetime]
    """
    pass


@overload
def get_unheld_classes(history: History, sample: str) -> list[str]:
    """
    Returns a list of unheld classes i.e., classes that are not part of the held_classes list.

    :return: (list[str]) - A list of datetime objects representing the unheld classes.
    :rtype: list[str]
    """
    pass


def get_unheld_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    return get_classes(history, "held", sample, False)


@overload
def get_held_classes(history: History, sample: datetime) -> list[datetime]:
    """
    Returns a list of held classes i.e., classes that are part of the held_classes list.

    :return: (list[datetime]) - A list of datetime objects representing the unheld classes.
    :rtype: list[datetime]
    """
    pass


@overload
def get_held_classes(history: History, sample: str) -> list[str]:
    """
    Returns a list of held classes i.e., classes that are part of the held_classes list.

    :return: (list[str]) - A list of datetime objects representing the unheld classes.
    :rtype: list[str]
    """
    pass


def get_held_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    return get_classes(history, "held", sample, True)


@overload
def get_unmarked_classes(history: History, sample: datetime) -> list[datetime]:
    """
    Returns a list of unmarked classes i.e., classes that are not part of the marked_classes list.

    :return: (list[datetime]) - A list of datetime objects representing the unmarked classes.
    :rtype: list[datetime]
    """
    pass


@overload
def get_unmarked_classes(history: History, sample: str) -> list[str]:
    """
    Returns a list of unmarked classes i.e., classes that are not part of the marked_classes list.

    :return: (list[str]) - A list of datetime objects representing the unmarked classes.
    :rtype: list[str]
    """
    pass


def get_unmarked_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    return get_classes(history, "marked", sample, False)


@overload
def get_marked_classes(history: History, sample: datetime) -> list[datetime]:
    """
    Returns a list of marked classes i.e., classes that are part of the marked_classes list.

    :return: (list[datetime]) - A list of datetime objects representing the marked classes.
    :rtype: list[datetime]
    """
    pass


@overload
def get_marked_classes(history: History, sample: str) -> list[str]:
    """
    Returns a list of marked classes i.e., classes that are part of the marked_classes list.

    :return: (list[str]) - A list of datetime objects representing the marked classes.
    :rtype: list[str]
    """
    pass


def get_marked_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    return get_classes(history, "marked", sample, True)


@overload
def get_unrecorded_classes(history: History, sample: str) -> list[str]:
    pass


@overload
def get_unrecorded_classes(history: History, sample: datetime) -> list[datetime]:
    pass


def get_unrecorded_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    if isinstance(sample, datetime):
        held_dates = get_held_classes(history, sample)
        unmarked_dates = get_unmarked_classes(history, sample)
        held_dates = parse_dates(held_dates).unwrap()
        unmarked_dates = parse_dates(unmarked_dates).unwrap()
    else:
        held_dates = get_held_classes(history, sample)
        unmarked_dates = get_unmarked_classes(history, sample)

    held_dates = set(held_dates)
    unmarked_dates = set(unmarked_dates)
    result = held_dates.intersection(unmarked_dates)
    result = list(result)
    result.sort()
    if isinstance(sample, str):
        return result

    return parse_dates(result).unwrap()

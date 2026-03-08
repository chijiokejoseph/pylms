from datetime import datetime
from typing import Literal, overload

from ..constants import DATE_FMT
from ..date import parse_dates
from ..errors import Result, eprint
from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from .dates_with_history import all_dates
from .history import History


def get_date_index(history: History, date: str) -> Result[int]:
    """Get the class number (1-based index) for a given date.

    Args:
        history (History): History instance containing dates.
        date (str): Date to find index for.

    Returns:
        Result[int]: Success with 1-based class number or error message.
    """
    dates = all_dates(history, "")
    if date not in dates:
        msg = f"{date} not in src: '{dates}'"
        eprint(msg)
        return Result.err(msg)

    return Result.ok(dates.index(date) + 1)


def get_class_info(history: History, class_date: str) -> Result[ClassFormInfo]:
    """Find ClassFormInfo that matches the given date.

    Args:
        history (History): History instance containing class forms.
        class_date (str): Date to match class form to.

    Returns:
        Result[ClassFormInfo]: Success with matching form or error message.
    """
    matched_forms = [form for form in history.class_forms if form.date == class_date]
    if len(matched_forms) == 0:
        msg = f"No class form matches the specified date: {class_date}"
        eprint(msg)
        return Result.err(msg)

    return Result.ok(matched_forms[0])


def get_available_class_forms(history: History) -> list[ClassFormInfo]:
    """Get list of class forms that have not been recorded yet.

    Args:
        history (History): History instance containing form information.

    Returns:
        list[ClassFormInfo]: List of available class forms.
    """
    return [
        form for form in history.class_forms if form not in history.recorded_class_forms
    ]


def get_available_cds_forms(history: History) -> list[CDSFormInfo]:
    """Get list of CDS forms that have not been recorded yet.

    Args:
        history (History): History instance containing form information.

    Returns:
        list[CDSFormInfo]: List of available CDS forms.
    """
    return [
        form for form in history.cds_forms if form not in history.recorded_cds_forms
    ]


def get_available_update_forms(history: History) -> list[UpdateFormInfo]:
    """Get list of update forms that have not been recorded yet.

    Args:
        history (History): History instance containing form information.

    Returns:
        list[UpdateFormInfo]: List of available update forms.
    """
    return [
        form
        for form in history.update_forms
        if form not in history.recorded_update_forms
    ]


def get_classes(
    history: History,
    prop: Literal["held", "marked"],
    sample: str | datetime,
    present: bool,
) -> list[str] | list[datetime]:
    """Get classes based on property and presence criteria.

    Args:
        history (History): History instance containing class information.
        prop (Literal["held", "marked"]): Property to check (held or marked).
        sample (str | datetime): Sample to determine return type.
        present (bool): Whether to return present or absent classes.

    Returns:
        list[str] | list[datetime]: List of classes matching criteria.
    """
    if prop == "held":
        dates = history.held_classes
        src = history.dates
    else:
        dates = history.marked_classes
        src = history.held_classes

    if isinstance(sample, datetime):
        if present:
            return dates
        else:
            return [date for date in src if date not in dates]
    else:
        if present:
            return [date.strftime(DATE_FMT) for date in dates]
        else:
            return [
                date.strftime(DATE_FMT) for date in src if date not in dates
            ]


@overload
def get_unheld_classes(history: History, sample: datetime) -> list[datetime]:
    pass


@overload
def get_unheld_classes(history: History, sample: str) -> list[str]:
    pass


def get_unheld_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    """Get list of classes that have not been held yet.

    Args:
        history (History): History instance containing class information.
        sample (str | datetime): Sample to determine return type.

    Returns:
        list[str] | list[datetime]: List of unheld classes.
    """
    return get_classes(history, "held", sample, False)


@overload
def get_held_classes(history: History, sample: str) -> list[str]:
    pass


@overload
def get_held_classes(history: History, sample: datetime) -> list[datetime]:
    pass


def get_held_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    """Get list of classes that have been held.

    Args:
        history (History): History instance containing class information.
        sample (str | datetime): Sample to determine return type.

    Returns:
        list[str] | list[datetime]: List of held classes.
    """
    return get_classes(history, "held", sample, True)


@overload
def get_unmarked_classes(history: History, sample: str) -> list[str]:
    pass


@overload
def get_unmarked_classes(history: History, sample: datetime) -> list[datetime]:
    pass


def get_unmarked_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    """Get list of classes that have not been marked for attendance.

    Args:
        history (History): History instance containing class information.
        sample (str | datetime): Sample to determine return type.

    Returns:
        list[str] | list[datetime]: List of unmarked classes.
    """
    return get_classes(history, "marked", sample, False)


@overload
def get_marked_classes(history: History, sample: str) -> list[str]:
    pass


@overload
def get_marked_classes(history: History, sample: datetime) -> list[datetime]:
    pass


def get_marked_classes(
    history: History, sample: str | datetime
) -> list[str] | list[datetime]:
    """Get list of classes that have been marked for attendance.

    Args:
        history (History): History instance containing class information.
        sample (str | datetime): Sample to determine return type.

    Returns:
        list[str] | list[datetime]: List of marked classes.
    """
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
    """Get list of classes that have been held but not marked for attendance.

    Args:
        history (History): History instance containing class information.
        sample (str | datetime): Sample to determine return type.

    Returns:
        list[str] | list[datetime]: List of unrecorded classes (held but not marked).
    """
    if isinstance(sample, datetime):
        held_dates = get_held_classes(history, sample)
        unmarked_dates = get_unmarked_classes(history, sample)
        held_dates = parse_dates(held_dates).unwrap()
        unmarked_dates = parse_dates(unmarked_dates).unwrap()
    else:
        held_dates = get_held_classes(history, sample)
        unmarked_dates = get_unmarked_classes(history, sample)

    # Find intersection of held and unmarked classes
    held_dates = set(held_dates)
    unmarked_dates = set(unmarked_dates)
    result = held_dates.intersection(unmarked_dates)
    result = list(result)
    result.sort()

    if isinstance(sample, str):
        return result

    return parse_dates(result).unwrap()

from datetime import datetime
from typing import Literal, overload

from ..date import parse_dates
from ..errors import Result, Unit, eprint
from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo, sort_form
from .dates_with_history import all_dates
from .history import History


@overload
def add_held_class(history: History, class_id: int) -> Result[Unit]:
    pass


@overload
def add_held_class(history: History, class_id: str) -> Result[Unit]:
    pass


def add_held_class(history: History, class_id: int | str) -> Result[Unit]:
    """Add a class to the held classes list.
    
    Args:
        history (History): History instance to update.
        class_id (int | str): Class number or date to add.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    return add_prop_class(history, "held", class_id)


@overload
def add_marked_class(history: History, class_id: int) -> Result[Unit]:
    pass


@overload
def add_marked_class(history: History, class_id: str) -> Result[Unit]:
    pass


def add_marked_class(history: History, class_id: int | str) -> Result[Unit]:
    """Add a class to the marked classes list.
    
    Args:
        history (History): History instance to update.
        class_id (int | str): Class number or date to add.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    return add_prop_class(history, "marked", class_id)


def add_prop_class(
    history: History, prop: Literal["held", "marked"], class_id: int | str
) -> Result[Unit]:
    """Add a class to held or marked classes list based on class number or date.
    
    Args:
        history (History): History instance to update.
        prop (Literal["held", "marked"]): Property to update (held or marked).
        class_id (int | str): Class number (1-based) or date string.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    # Ensure dates have been updated
    if not history.updated:
        msg = "Dates must be updated before adding marked classes."
        eprint(msg)
        return Result.err(msg)

    # Convert class_id to class number
    if isinstance(class_id, int):
        if class_id < 1 or class_id > len(history.dates):
            msg = f"Class number {class_id} is out of range."
            eprint(msg)
            return Result.err(msg)
        class_num: int = class_id
    else:
        if class_id not in all_dates(history, ""):
            msg = f"Class Date: {class_id} is not part of the valid dates list for this program."
            eprint(msg)
            return Result.err(msg)
        class_num = all_dates(history, "").index(class_id) + 1

    # Get target date
    target_date: datetime = history.dates[class_num - 1]
    target_date_str: str = all_dates(history, "")[class_num - 1]

    if prop == "held":
        history.held_classes.append(target_date)
        history.held_classes.sort()
    else:
        # Check if class has been held before marking
        held_classes = parse_dates(history.held_classes)
        if held_classes.is_err():
            return held_classes.propagate()
        held_classes = held_classes.unwrap()

        if target_date_str not in held_classes:
            msg = f"Specified class date: {target_date_str} has not been held yet and cannot be marked if not held."
            eprint(msg)
            return Result.err(msg)

        history.marked_classes.append(target_date)
        history.marked_classes.sort()

    return Result.unit()


def add_cds_form(history: History, form: CDSFormInfo) -> None:
    """Add CDS form to the list of CDS forms.
    
    Args:
        history (History): History instance to update.
        form (CDSFormInfo): CDS form to add.
    """
    history.cds_forms.append(form)
    history.cds_forms.sort(key=sort_form)


def add_recorded_cds_form(history: History, form: CDSFormInfo) -> None:
    """Add recorded CDS form to the list of recorded CDS forms.
    
    Args:
        history (History): History instance to update.
        form (CDSFormInfo): Recorded CDS form to add.
    """
    history.recorded_cds_forms.append(form)
    history.recorded_cds_forms.sort(key=sort_form)


def add_update_form(history: History, form: UpdateFormInfo) -> None:
    """Add update form to the list of update forms.
    
    Args:
        history (History): History instance to update.
        form (UpdateFormInfo): Update form to add.
    """
    history.update_forms.append(form)
    history.update_forms.sort(key=sort_form)


def add_recorded_update_form(history: History, form: UpdateFormInfo) -> None:
    """Add recorded update form to the list of recorded update forms.
    
    Args:
        history (History): History instance to update.
        form (UpdateFormInfo): Recorded update form to add.
    """
    history.recorded_update_forms.append(form)
    history.recorded_update_forms.sort(key=sort_form)


def add_class_form(history: History, form: ClassFormInfo) -> None:
    """Add class form to the list of class forms.
    
    Args:
        history (History): History instance to update.
        form (ClassFormInfo): Class form to add.
    """
    history.class_forms.append(form)
    history.class_forms.sort(key=sort_form)


def add_recorded_class_form(history: History, form: ClassFormInfo) -> None:
    """Add recorded class form to the list of recorded class forms.
    
    Args:
        history (History): History instance to update.
        form (ClassFormInfo): Recorded class form to add.
    """
    history.recorded_class_forms.append(form)
    history.recorded_class_forms.sort(key=sort_form)

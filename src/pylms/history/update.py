from datetime import datetime
from typing import Literal, overload

from ..errors import Result, Unit, eprint
from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from .dateutil import all_dates
from .history import History


@overload
def add_held_class(history: History, class_id: int) -> Result[Unit]:
    pass


@overload
def add_held_class(history: History, class_id: str) -> Result[Unit]:
    pass


def add_held_class(history: History, class_id: int | str) -> Result[Unit]:
    return add_prop_class(history, "held", class_id)


@overload
def add_marked_class(history: History, class_id: int) -> Result[Unit]:
    pass


@overload
def add_marked_class(history: History, class_id: str) -> Result[Unit]:
    pass


def add_marked_class(history: History, class_id: int | str) -> Result[Unit]:
    return add_prop_class(history, "marked", class_id)


def add_prop_class(
    history: History, prop: Literal["held", "marked"], class_id: int | str
) -> Result[Unit]:
    """Adds a marked class based on the class number. Either class_num or class_date must be specified, else an error will be raised.

    :param class_num: (int | None) - The
        class number to add as a held class. Defaults to None.
    :type class_num: int | None

    :param class_date: (str | None) - The
        class date to add as a held class. Defaults to None.
    :type class_date: str | None

    :return: (Result[Unit]) - a result object.
    :rtype: Result[Unit]


    """
    # Ensure that dates have been updated before adding marked classes
    if not history.updated:
        msg = "Dates must be updated before adding marked classes."
        eprint(msg)
        return Result.err(msg)

    # Check if the class number is within the valid range
    if isinstance(class_id, int):
        if class_id < 1 or class_id > len(history.dates):
            msg = f"Class number {class_id} is out of range."
            eprint(msg)
            return Result.err(msg)
        else:
            class_num: int = class_id

    else:
        if class_id not in all_dates(history, ""):
            msg = f"Class Date: {class_id} is not part of the valid dates list for this program."
            eprint(msg)
            return Result.err(msg)
        else:
            class_num = all_dates(history, "").index(class_id)

    # Get the date corresponding to the class number and add it to held classes
    target_date: datetime = history.dates[class_num - 1]

    if prop == "held":
        history.held_classes.append(target_date)
    else:
        history.marked_classes.append(target_date)

    return Result.unit()


def add_cds_form(history: History, form: CDSFormInfo) -> None:
    """
    Adds a CDS Form to the list of CDS forms.

    :param form: (CDSFormInfo) - The CDS Form to add.
    :type form: CDSFormInfo
    :return: (None) - This method does not return anything.
    :rtype: None
    """
    history.cds_forms.append(form)


def add_recorded_cds_form(history: History, form: CDSFormInfo) -> None:
    """
    Adds a recorded CDS Form to the list of recorded CDS forms.

    :param form: (CDSFormInfo) - The recorded CDS Form to add.
    :type form: CDSFormInfo
    :return: (None) - This method does not return anything.
    :rtype: None
    """
    history.recorded_cds_forms.append(form)


def add_update_form(history: History, form: UpdateFormInfo) -> None:
    """
    Adds an Update Form to the list of Update forms.

    :param form: (UpdateFormInfo) - The Update Form to add.
    :type form: UpdateFormInfo
    :return: (None) - This method does not return anything.
    :rtype: None
    """
    history.update_forms.append(form)


def add_recorded_update_form(history: History, form: UpdateFormInfo) -> None:
    """
    Adds a recorded Update Form to the list of recorded Update forms.

    :param form: (UpdateFormInfo) - The recorded Update Form to add.
    :type form: UpdateFormInfo
    :return: (None) - This method does not return anything.
    :rtype: None
    """
    history.recorded_update_forms.append(form)


def add_class_form(history: History, form: ClassFormInfo) -> None:
    """
    Adds a Class Form to the list of Class forms.

    :param form: (ClassFormInfo) - The Class Form to add.
    :type form: ClassFormInfo
    :return: (None) - This method does not return anything.
    :rtype: None
    """
    history.class_forms.append(form)


def add_recorded_class_form(history: History, form: ClassFormInfo) -> None:
    """
    Adds a recorded Class Form to the list of recorded Class forms.

    :param form: (ClassFormInfo) - The recorded Class Form to add.
    :type form: ClassFormInfo
    :return: (None) - This method does not return anything.
    :rtype: None
    """
    history.recorded_class_forms.append(form)

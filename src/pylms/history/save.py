import json

from ..constants import DATE_FMT, HISTORY_PATH
from ..errors import Result, Unit
from ..paths import get_history_path
from .history import History


def save_history(history: History) -> Result[Unit]:
    """Saves the current history data to a JSON file.

    :return: (Result[Unit]) - a result object.
    :rtype: Result[Unit]

    """
    data = {
        # Cohort number
        "cohort": history.cohort,
        # List of 3 integers representing weekdays on which classes are held
        "class_days": list(history.class_days),
        # List of 3 integers representing weekdays on which classes are marked
        "dates": [date.strftime(DATE_FMT) for date in history.dates],
        # orientation date in the format specified by DATE_FMT or None
        "orientation_date": history.orientation_date.strftime(DATE_FMT)
        if history.orientation_date is not None
        else None,
        # Number of weeks the course lasts
        "weeks": history.weeks,
        # Interlude if present
        "interlude": history.interlude.to_dict()
        if history.interlude is not None
        else {},
        # List of classes for which attendance has been generated
        "held_classes": [date.strftime(DATE_FMT) for date in history.held_classes],
        # List of classes for which attendance has been marked
        "marked_classes": [date.strftime(DATE_FMT) for date in history.marked_classes],
        # List of dictionaries representing ClassFormInfo objects
        "class_forms": [data.model_dump(mode="json") for data in history.class_forms],
        # List of dictionaries representing ClassFormInfo objects for
        # recorded classes
        "recorded_class_forms": [
            data.model_dump(mode="json") for data in history.recorded_class_forms
        ],
        # List of dictionaries representing CDSFormInfo objects
        "cds_forms": [data.model_dump(mode="json") for data in history.cds_forms],
        # List of dictionaries representing CDSFormInfo objects
        # for recorded CDS forms
        "recorded_cds_forms": [
            data.model_dump(mode="json") for data in history.recorded_cds_forms
        ],
        # List of dictionaries representing UpdateFormInfo objects
        "update_forms": [data.model_dump(mode="json") for data in history.update_forms],
        # List of dictionaries representing UpdateFormInfo objects
        # for recorded update forms
        "recorded_update_forms": [
            data.model_dump(mode="json") for data in history.recorded_update_forms
        ],
        "attendance": [
            history.attendance[0],
            str(history.attendance[1]),
        ],  # List of boolean and file path
        "assessment": [
            history.assessment[0],
            str(history.assessment[1]),
        ],  # List of boolean and file path
        "project": [
            history.project[0],
            str(history.project[1]),
        ],  # List of boolean and file path
        "result": [
            history.result[0],
            str(history.result[1]),
        ],  # List of boolean and file path
        "merit": [
            history.merit[0],
            str(history.merit[1]),
        ],  # List of boolean and file path
    }

    # Save the history data to the JSON file
    with get_history_path().open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    # Save the history data to the JSON file
    with HISTORY_PATH.open("w") as file:
        json.dump(data, file, indent=2)

    return Result.unit()

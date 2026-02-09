import json

from ..constants import DATE_FMT, HISTORY_PATH
from ..errors import Result, Unit
from ..paths import get_history_path
from .history import History


def save_history(history: History) -> Result[Unit]:
    """Save current history data to JSON file.

    Saves history data to both the main history file and updates the dates
    JSON file if dates have changed.

    Args:
        history (History): History instance to save.

    Returns:
        Result[Unit]: Success or error message.
    """

    from ..paths_state import display_path

    data = {
        "cohort": history.cohort,
        "class_days": list(history.class_days),
        "dates": [date.strftime(DATE_FMT) for date in history.dates],
        "orientation_date": history.orientation_date.strftime(DATE_FMT)
        if history.orientation_date is not None
        else None,
        "weeks": history.weeks,
        "interlude": history.interlude.to_dict()
        if history.interlude is not None
        else None,
        "held_classes": [date.strftime(DATE_FMT) for date in history.held_classes],
        "marked_classes": [date.strftime(DATE_FMT) for date in history.marked_classes],
        "class_forms": [data.model_dump(mode="json") for data in history.class_forms],
        "recorded_class_forms": [
            data.model_dump(mode="json") for data in history.recorded_class_forms
        ],
        "cds_forms": [data.model_dump(mode="json") for data in history.cds_forms],
        "recorded_cds_forms": [
            data.model_dump(mode="json") for data in history.recorded_cds_forms
        ],
        "update_forms": [data.model_dump(mode="json") for data in history.update_forms],
        "recorded_update_forms": [
            data.model_dump(mode="json") for data in history.recorded_update_forms
        ],
        "attendance": [history.attendance[0], str(history.attendance[1])],
        "assessment": [history.assessment[0], str(history.assessment[1])],
        "project": [history.project[0], str(history.project[1])],
        "result": [history.result[0], str(history.result[1])],
        "merit": [history.merit[0], str(history.merit[1])],
    }

    # Save history data to JSON files
    with get_history_path().open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    with HISTORY_PATH.open("w") as file:
        json.dump(data, file, indent=2)

    display_path("History")
    return Result.unit()

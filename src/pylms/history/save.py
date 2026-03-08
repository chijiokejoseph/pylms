import json

from ..config import Config
from ..constants import DATE_FMT, HISTORY_PATH
from ..errors import Result, Unit
from ..paths import display_path, get_history_path
from .history import History


def save_history(config: Config, history: History) -> Result[Unit]:
    """Save current history data to JSON file.

    Args:
        config: Application configuration.
        history: History instance to save.

    Returns:
        Result[Unit]: Success or error message.
    """
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
        "class_forms": [form.model_dump(mode="json") for form in history.class_forms],
        "recorded_class_forms": [
            form.model_dump(mode="json") for form in history.recorded_class_forms
        ],
        "cds_forms": [form.model_dump(mode="json") for form in history.cds_forms],
        "recorded_cds_forms": [
            form.model_dump(mode="json") for form in history.recorded_cds_forms
        ],
        "update_forms": [form.model_dump(mode="json") for form in history.update_forms],
        "recorded_update_forms": [
            form.model_dump(mode="json") for form in history.recorded_update_forms
        ],
        "group": history.group,
        "attendance": [history.attendance[0], str(history.attendance[1])],
        "assessment": [history.assessment[0], str(history.assessment[1])],
        "project": [history.project[0], str(history.project[1])],
        "result": [history.result[0], str(history.result[1])],
        "merit": [history.merit[0], str(history.merit[1])],
    }

    # Save history data to JSON files
    with get_history_path(config).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    with HISTORY_PATH.open("w") as file:
        json.dump(data, file, indent=2)

    display_path(config, "History")
    return Result.unit()

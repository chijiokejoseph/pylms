import json
from pathlib import Path

from ..constants import DATE_FMT, HISTORY_PATH
from ..errors import Result, Unit, eprint
from ..paths import get_history_path, get_paths_json
from .dates_with_history import all_dates
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

    # Update dates JSON file if needed
    dates_json_path: Path = get_paths_json()["Date"]

    if not dates_json_path.exists():
        # Create dates JSON file
        with dates_json_path.open("w") as file:
            json.dump(all_dates(history, ""), file, indent=2)
        return Result.unit()

    # Load existing dates and compare
    dates_json_list: list[str] = []
    with dates_json_path.open("r") as file:
        dates_data = json.load(file)
        if not isinstance(dates_data, list):
            msg = "dates_data is not a list"
            eprint(msg)
            return Result.err(msg)
        if len(dates_data) != 0 and not all(
            isinstance(value, str) for value in dates_data
        ):
            msg = "dates_data is not a list"
            eprint(msg)
            return Result.err(msg)

        dates_json_list.extend(dates_data)

    # Update dates file if changed
    if dates_json_list != all_dates(history, ""):
        with dates_json_path.open("w") as file:
            json.dump(all_dates(history, ""), file, indent=2)

    return Result.unit()

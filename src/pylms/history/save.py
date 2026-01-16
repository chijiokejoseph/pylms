import json
from pathlib import Path

from ..constants import DATE_FMT, HISTORY_PATH
from ..errors import Result, Unit, eprint
from ..paths import get_history_path, get_paths_json
from .dates_with_history import all_dates
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
        else None,
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

    # Save the dates to the JSON file (`Json/dates.json`)
    # if the dates have changed

    # Get `Json/dates.json`
    dates_json_path: Path = get_paths_json()["Date"]

    # Check if `Json/dates.json` exists
    if not dates_json_path.exists():
        # Create `Json/dates.json`, save the dates and return
        with dates_json_path.open("w") as file:
            json.dump(all_dates(history, ""), file, indent=2)
        return Result.unit()

    # Load the dates from the JSON file `Json/dates.json`
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

    # Update the dates in the JSON file if they have changed
    if dates_json_list != all_dates(history, ""):
        with dates_json_path.open("w") as file:
            json.dump(all_dates(history, ""), file, indent=2)

    return Result.unit()

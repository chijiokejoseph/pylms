import json
from datetime import datetime
from pathlib import Path

from ..date import parse_dates, to_date
from ..errors import Result, eprint
from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from ..paths import get_history_path
from .classes import sync_classes
from .history import History
from .interlude import Interlude


def load_history() -> Result[History]:
    """Load history data from JSON file and initialize History object.
    
    Returns:
        Result[History]: Success with loaded History instance or error message.
    """
    history = History()
    history_path: Path = get_history_path()

    if not history_path.exists():
        msg = f"path to history.json '{history_path}' does not exist"
        eprint(msg)
        return Result.err(msg)

    # Read history data from JSON file
    with history_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # Validate data format
    if not isinstance(data, dict):
        msg = "Invalid history data format."
        eprint(msg)
        return Result.err(msg)

    # Load and validate each attribute
    if "cohort" in data:
        if not isinstance(data["cohort"], int):
            msg = "Cohort must be an integer."
            eprint(msg)
            return Result.err(msg)
        history.cohort = data["cohort"]

    if "class_days" in data:
        if not isinstance(data["class_days"], list) or len(data["class_days"]) != 3:
            msg = "Class dates must be a list of exactly 3 integers."
            eprint(msg)
            return Result.err(msg)
        if not all(isinstance(num, int) for num in data["class_days"]):
            msg = "All class dates must be integers."
            eprint(msg)
            return Result.err(msg)
        history.class_days = [num for num in data["class_days"]]

    if "dates" in data:
        if not isinstance(data["dates"], list):
            msg = "Dates must be a list of date strings."
            eprint(msg)
            return Result.err(msg)
        if len(data["dates"]) == 0:
            msg = "Dates must have more than one element"
            eprint(msg)
            return Result.err(msg)
        dates = parse_dates(data["dates"])
        if dates.is_err():
            return dates.propagate()
        history.dates = dates.unwrap()

    if "orientation_date" in data:
        orientation_date = data["orientation_date"]
        if orientation_date is None:
            msg = "orientation_date is not set"
            eprint(msg)
            return Result.err(msg)
        if not isinstance(orientation_date, str):
            msg = "orientation_date is expected to be a `str`."
            eprint(msg)
            return Result.err(msg)
        date = to_date(orientation_date)
        if date.is_err():
            return date.propagate()
        date = date.unwrap()
        history.orientation_date = date

    if "weeks" in data:
        if not isinstance(data["weeks"], int) or data["weeks"] < 1:
            msg = "Weeks must be a positive integer."
            eprint(msg)
            return Result.err(msg)
        history.weeks = data["weeks"]

    if "interlude" in data:
        interlude = Interlude.from_dict(data["interlude"])
        if interlude.is_err():
            return interlude.propagate()
        history.interlude = interlude.unwrap()

    if "held_classes" in data:
        if not isinstance(data["held_classes"], list):
            msg = "Held classes must be a list of date strings."
            eprint(msg)
            return Result.err(msg)
        dates = parse_dates(data["held_classes"])
        if dates.is_err():
            return dates.propagate()
        history.held_classes = dates.unwrap()

    if "marked_classes" in data:
        if not isinstance(data["marked_classes"], list):
            msg = "Marked classes must be a list of date strings."
            eprint(msg)
            return Result.err(msg)
        datetimes: list[datetime] = []
        raw_dates: list[str] = data["marked_classes"]
        for date_str in raw_dates:
            value = to_date(date_str)
            if value.is_err():
                return value.propagate()
            value = value.unwrap()
            datetimes.append(value)
        dates = parse_dates(raw_dates)
        if dates.is_err():
            return dates.propagate()
        history.marked_classes = dates.unwrap()

    # Load form information
    if "class_forms" in data:
        if not isinstance(data["class_forms"], list) and not isinstance(
            data["class_forms"][0], dict
        ):
            msg = "Class forms must be a list of dictionaries"
            eprint(msg)
            return Result.err(msg)
        history.class_forms = [
            ClassFormInfo.model_validate(info) for info in data["class_forms"]
        ]

    if "recorded_class_forms" in data:
        if not isinstance(data["recorded_class_forms"], list) and not isinstance(
            data["recorded_class_forms"][0], dict
        ):
            msg = "Class forms must be a list of dictionaries"
            eprint(msg)
            return Result.err(msg)
        history.recorded_class_forms = [
            ClassFormInfo.model_validate(info) for info in data["recorded_class_forms"]
        ]

    if "cds_forms" in data:
        if not isinstance(data["cds_forms"], list) and not isinstance(
            data["cds_forms"][0], dict
        ):
            msg = "CDS forms must be a list of dictionaries"
            eprint(msg)
            return Result.err(msg)
        history.cds_forms = [
            CDSFormInfo.model_validate(info) for info in data["cds_forms"]
        ]

    if "recorded_cds_forms" in data:
        if not isinstance(data["recorded_cds_forms"], list) and not isinstance(
            data["recorded_cds_forms"][0], dict
        ):
            msg = "CDS forms must be a list of dictionaries"
            eprint(msg)
            return Result.err(msg)
        history.recorded_cds_forms = [
            CDSFormInfo.model_validate(info) for info in data["recorded_cds_forms"]
        ]

    if "update_forms" in data:
        if not isinstance(data["update_forms"], list) and not isinstance(
            data["update_forms"][0], dict
        ):
            msg = "Update forms must be a list of dictionaries"
            eprint(msg)
            return Result.err(msg)
        history.update_forms = [
            UpdateFormInfo.model_validate(info) for info in data["update_forms"]
        ]

    if "recorded_update_forms" in data:
        if not isinstance(data["recorded_update_forms"], list) and not isinstance(
            data["recorded_update_forms"][0], dict
        ):
            msg = "Update forms must be a list of dictionaries"
            eprint(msg)
            return Result.err(msg)
        history.recorded_update_forms = [
            UpdateFormInfo.model_validate(info)
            for info in data["recorded_update_forms"]
        ]

    # Load collation status and paths
    if "attendance" in data:
        if not isinstance(data["attendance"], list) or len(data["attendance"]) != 2:
            msg = "Attendance must be a list with two elements: a boolean and a file path."
            eprint(msg)
            return Result.err(msg)
        history.attendance = (data["attendance"][0], Path(data["attendance"][1]))

    if "assessment" in data:
        if not isinstance(data["assessment"], list) or len(data["assessment"]) != 2:
            msg = "Assessment must be a list with two elements: a boolean and a file path."
            eprint(msg)
            return Result.err(msg)
        history.assessment = (data["assessment"][0], Path(data["assessment"][1]))

    if "project" in data:
        if not isinstance(data["project"], list) or len(data["project"]) != 2:
            msg = "Project must be a list with two elements: a boolean and a file path."
            eprint(msg)
            return Result.err(msg)
        history.project = (data["project"][0], Path(data["project"][1]))

    if "result" in data:
        if not isinstance(data["result"], list) or len(data["result"]) != 2:
            msg = "Result must be a list with two elements: a boolean and a file path."
            eprint(msg)
            return Result.err(msg)
        history.result = (data["result"][0], Path(data["result"][1]))

    if "merit" in data:
        if not isinstance(data["merit"], list) or len(data["merit"]) != 2:
            msg = "Merit must be a list with two elements: a boolean and a file path."
            eprint(msg)
            return Result.err(msg)
        history.merit = (data["merit"][0], Path(data["merit"][1]))

    # Sync classes based on loaded data
    result = sync_classes(history)
    if result.is_err():
        return result.propagate()

    return Result.ok(history)

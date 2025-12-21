import json
from datetime import datetime
from pathlib import Path

from ..date import parse_dates, to_date
from ..errors import Result, eprint
from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from ..paths import get_history_path
from .days_cohort import update_dates
from .history import History


def load_history() -> Result[History]:
    """Loads the history data from a JSON file and initializes the History object.
    :return: (History) - An instance of the History class with loaded data.
    :rtype: History


    """
    history = History()
    history_path: Path = get_history_path()

    if not history_path.exists():
        msg = f"path to history.json '{history_path}' does not exist"
        eprint(msg)
        return Result.err(msg)

    # Read the history data from the JSON file
    with history_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # Validate the data format
    if not isinstance(data, dict):
        msg = "Invalid history data format."
        eprint(msg)
        return Result.err(msg)

    # Check and set attribute `cohort`
    if "cohort" in data:
        if not isinstance(data["cohort"], int):
            msg = "Cohort must be an integer."
            eprint(msg)
            return Result.err(msg)

        history.cohort = data["cohort"]

    # Check and set attribute `class_days`
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

    # Check and set attribute `dates`
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

    # Check and set attribute `orientation_date`
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

    # Check and set attribute `weeks`
    if "weeks" in data:
        if not isinstance(data["weeks"], int) or data["weeks"] < 1:
            msg = "Weeks must be a positive integer."
            eprint(msg)
            return Result.err(msg)
        history.weeks = data["weeks"]

    # Check and set attribute `held_classes`
    if "held_classes" in data:
        if not isinstance(data["held_classes"], list):
            msg = "Held classes must be a list of date strings."
            eprint(msg)
            return Result.err(msg)
        dates = parse_dates(data["held_classes"])
        if dates.is_err():
            return dates.propagate()

        history.held_classes = dates.unwrap()

    # Check and set attribute `marked_classes`
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

    # Check and set attribute `class_forms`
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

    # Check and set attribute `recorded_class_forms`
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

    # Check and set attribute `cds_forms`
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

    # Check and set attribute `recorded_cds_forms`
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

    # Check and set attribute `update_forms`
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

    # Check and set attribute `recorded_update_forms`
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

    # Check and set attributes `attendance`, `assessment`, `project`, and `result`
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

    # Update the dates based on the loaded data
    result = update_dates(history)
    if result.is_err():
        return result.propagate()

    return Result.ok(history)

"""Test fixtures and helpers for History unit tests."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..constants import DATE_FMT
from ..date import parse_dates, to_date
from ..errors import Result
from ..models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from .history import History
from .interlude import Interlude


def create_test_history(
    orientation_date: datetime | None = None,
    weeks: int = 12,
    class_days: list[int] | None = None,
    interlude: Interlude | None = None,
) -> History:
    """Create a test History instance with default or custom values.

    Args:
        orientation_date: Orientation date (defaults to 2025-01-01).
        weeks: Number of weeks (defaults to 12).
        class_days: Class weekdays (defaults to [0, 2, 4] - Mon, Wed, Fri).
        interlude: Optional interlude period.

    Returns:
        History: Configured test History instance.
    """
    if orientation_date is None:
        orientation_date = datetime(2025, 1, 1)

    if class_days is None:
        class_days = [0, 2, 4]

    history = History()
    history.orientation_date = orientation_date
    history.weeks = weeks
    history.class_days = class_days
    history.interlude = interlude

    return history


def save_test_history(history: History, path: Path) -> Result[None]:
    """Save history to a custom test path.

    Args:
        history: History instance to save.
        path: Custom file path for test data.

    Returns:
        Result[None]: Success or error.
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
        "attendance": [history.attendance[0], str(history.attendance[1])],
        "assessment": [history.assessment[0], str(history.assessment[1])],
        "project": [history.project[0], str(history.project[1])],
        "result": [history.result[0], str(history.result[1])],
        "merit": [history.merit[0], str(history.merit[1])],
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return Result.ok(None)


def load_test_history(path: Path) -> Result[History]:
    """Load history from a custom test path.

    Args:
        path: Custom file path for test data.

    Returns:
        Result[History]: Loaded History instance or error.
    """
    if not path.exists():
        return Result.err(f"Test history file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data: dict[str, Any] = json.load(file)

    history = History()

    if "cohort" in data:
        history.cohort = data["cohort"]

    if "class_days" in data:
        history.class_days = data["class_days"]

    if "dates" in data and isinstance(data["dates"], list):
        dates = parse_dates(data["dates"])
        if dates.is_err():
            return dates.propagate()
        history.dates = dates.unwrap()

    if "orientation_date" in data and isinstance(data["orientation_date"], str):
        date = to_date(data["orientation_date"])
        if date.is_err():
            return date.propagate()
        history.orientation_date = date.unwrap()

    if "weeks" in data:
        history.weeks = data["weeks"]

    if "interlude" in data and data["interlude"]:
        interlude = Interlude.from_dict(data["interlude"])
        if interlude.is_err():
            return interlude.propagate()
        history.interlude = interlude.unwrap()

    if "held_classes" in data and isinstance(data["held_classes"], list):
        dates = parse_dates(data["held_classes"])
        if dates.is_err():
            return dates.propagate()
        history.held_classes = dates.unwrap()

    if "marked_classes" in data and isinstance(data["marked_classes"], list):
        dates = parse_dates(data["marked_classes"])
        if dates.is_err():
            return dates.propagate()
        history.marked_classes = dates.unwrap()

    if "class_forms" in data:
        history.class_forms = [
            ClassFormInfo.model_validate(info) for info in data["class_forms"]
        ]

    if "recorded_class_forms" in data:
        history.recorded_class_forms = [
            ClassFormInfo.model_validate(info) for info in data["recorded_class_forms"]
        ]

    if "cds_forms" in data:
        history.cds_forms = [
            CDSFormInfo.model_validate(info) for info in data["cds_forms"]
        ]

    if "recorded_cds_forms" in data:
        history.recorded_cds_forms = [
            CDSFormInfo.model_validate(info) for info in data["recorded_cds_forms"]
        ]

    if "update_forms" in data:
        history.update_forms = [
            UpdateFormInfo.model_validate(info) for info in data["update_forms"]
        ]

    if "recorded_update_forms" in data:
        history.recorded_update_forms = [
            UpdateFormInfo.model_validate(info)
            for info in data["recorded_update_forms"]
        ]

    if "attendance" in data:
        history.attendance = (data["attendance"][0], Path(data["attendance"][1]))

    if "assessment" in data:
        history.assessment = (data["assessment"][0], Path(data["assessment"][1]))

    if "project" in data:
        history.project = (data["project"][0], Path(data["project"][1]))

    if "result" in data:
        history.result = (data["result"][0], Path(data["result"][1]))

    if "merit" in data:
        history.merit = (data["merit"][0], Path(data["merit"][1]))

    return Result.ok(history)

from pathlib import Path

from ..errors import Result, Unit, eprint
from ..paths import get_merit_path, get_paths_excel
from .history import History


def record_assessment(history: History) -> None:
    """
    Records the assessment by checking the existence of the Assessment.xlsx file
    and updates the `assessment` attribute with a tuple containing the existence
    status and the file path.

    :return: (None) - This method does not return anything.
    :rtype: None
    """
    path: Path = get_paths_excel()["Assessment"]
    history.assessment = (path.exists(), path)


def record_attendance(history: History) -> None:
    """
    Records the attendance by checking the existence of the Attendance.xlsx file
    and updates the `attendance` attribute with a tuple containing the existence
    status and the file path.

    :return: (None) - This method does not return anything.
    :rtype: None
    """
    path = get_paths_excel()["Attendance"]
    history.attendance = (path.exists(), path)


def record_project(history: History) -> None:
    """
    Records the project by checking the existence of the Project.xlsx file
    and updates the `project` attribute with a tuple containing the existence
    status and the file path.

    :return: (None) - This method does not return anything.
    :rtype: None
    """
    path = get_paths_excel()["Project"]
    history.project = (path.exists(), path)


def record_result(history: History) -> None:
    """
    Records the result by checking the existence of the Result.xlsx file
    and updates the `result` attribute with a tuple containing the existence
    status and the file path.

    :return: (None) - This method does not return anything.
    :rtype: None
    """
    path = get_paths_excel()["Result"]
    history.result = (path.exists(), path)


def record_merit(history: History) -> Result[Unit]:
    """
    Records the merit by checking the existence of the Merit.xlsx file
    and updates the `merit` attribute with a tuple containing the existence
    status and the file path.

    :return: (Result[Unit]) - a result object.
    :rtype: Result[Unit]
    """
    if history.cohort is None:
        msg = "Cohort is not set"
        eprint(msg)
        return Result.err(msg)

    path = get_merit_path(history.cohort)
    if path.is_err():
        return path.propagate()

    path = path.unwrap()

    history.merit = (path.exists(), path)
    return Result.unit()

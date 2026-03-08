from pathlib import Path

from ..config import Config
from ..errors import Result, Unit, eprint
from ..paths import get_merit_path, get_paths_excel
from .history import History


def record_assessment(config: Config, history: History) -> None:
    """Record assessment status by checking Assessment.xlsx file existence.

    Args:
        config (Config): Application Configuration settings
        history (History): History instance to update.
    """
    path: Path = get_paths_excel(
        config,
    )["Assessment"]
    history.assessment = (path.exists(), path)


def record_attendance(config: Config, history: History) -> None:
    """Record attendance status by checking Attendance.xlsx file existence.

    Args:
        config (Config): Application Configuration settings
        history (History): History instance to update.
    """
    path = get_paths_excel(config)["Attendance"]
    history.attendance = (path.exists(), path)


def record_project(config: Config, history: History) -> None:
    """Record project status by checking Project.xlsx file existence.

    Args:
        config (Config): Application Configuration settings
        history (History): History instance to update.
    """
    path = get_paths_excel(config)["Project"]
    history.project = (path.exists(), path)


def record_result(config: Config, history: History) -> None:
    """Record result status by checking Result.xlsx file existence.

    Args:
        config (Config): Application Configuration settings
        history (History): History instance to update.
    """
    path = get_paths_excel(config)["Result"]
    history.result = (path.exists(), path)


def record_merit(config: Config, history: History) -> Result[Unit]:
    """Record merit status by checking Merit.xlsx file existence.

    Args:
        config (Config): Application Configuration settings
        history (History): History instance to update.

    Returns:
        Result[Unit]: Success or error message.
    """
    if history.cohort is None:
        msg = "Cohort is not set"
        eprint(msg)
        return Result.err(msg)

    path = get_merit_path(config, history.cohort)
    if path.is_err():
        return path.propagate()

    path = path.unwrap()
    history.merit = (path.exists(), path)
    return Result.unit()

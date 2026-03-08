from pathlib import Path
from typing import Literal

from ..config import Config
from ..constants import GROUP
from .path_fns import get_excel_path


def get_grade_dir(config: Config) -> Path:
    return get_excel_path(config) / "grades"


def get_grade_path(config: Config, group_label: int | None = None) -> Path:
    if group_label is None:
        return get_grade_dir(config) / "Grading.xlsx"

    grade_dir: Path = get_grade_dir(config)
    grade_dir.mkdir(parents=True, exist_ok=True)
    return grade_dir / f"{GROUP}{group_label} Attendance.xlsx"


def get_grading_leader(config: Config, category: Literal["Leader", "Assistant"]) -> Path:
    return get_grade_dir(config) / f"{category}s.xlsx"

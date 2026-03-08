from pathlib import Path

from ..config import Config
from .path_fns import get_excel_path


def get_cohort_path(config: Config, cohort_no: int) -> Path:
    return get_excel_path(config) / f"Cohort {cohort_no} Python Beginners Attendance.xlsx"

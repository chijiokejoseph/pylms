from pathlib import Path

from ..config import Config
from .path_fns import get_excel_path


def get_list_path(config: Config, cohort_num: int) -> Path:
    return get_excel_path(config) / f"Cohort {cohort_num} Python Beginners Records.xlsx"

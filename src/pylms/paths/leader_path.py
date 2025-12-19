from pathlib import Path
from typing import Literal

from .group_data_path import get_group_dir
from .path_fns import get_excel_path


def get_criterion_path() -> Path:
    return get_excel_path() / "criterion"


def get_leader_path(category: Literal["Leader", "Assistant"]) -> Path:
    return get_group_dir() / f"{category}s.xlsx"


def get_group_criterion_path(group_num: int) -> Path:
    return get_criterion_path() / f"Group{group_num}.xlsx"

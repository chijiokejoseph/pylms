from pathlib import Path
from typing import Literal

from ..config import Config
from .group_data_path import get_group_dir
from .path_fns import get_excel_path


def get_criterion_path(config: Config) -> Path:
    return get_excel_path(config) / "criterion"


def get_leader_path(config: Config, category: Literal["Leader", "Assistant"]) -> Path:
    return get_group_dir(config) / f"{category}s.xlsx"


def get_group_criterion_path(config: Config, group_num: int) -> Path:
    return get_criterion_path(config) / f"Group{group_num}.xlsx"

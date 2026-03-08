from pathlib import Path

from ..config import Config
from ..constants import GROUP
from .path_fns import get_excel_path


def get_group_dir(config: Config) -> Path:
    return get_excel_path(config) / "groups"


def get_group_path(config: Config, group_label: int | None = None) -> Path:
    if group_label is None:
        return get_group_dir(config) / "Group.xlsx"

    group_dir: Path = get_group_dir(config)
    group_dir.mkdir(parents=True, exist_ok=True)
    return group_dir / f"{GROUP}{group_label}.xlsx"

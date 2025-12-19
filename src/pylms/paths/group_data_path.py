from pathlib import Path

from ..constants import GROUP
from .path_fns import get_excel_path


def get_group_dir() -> Path:
    return get_excel_path() / "groups"


def get_group_path(group_label: int | None = None) -> Path:
    if group_label is None:
        return get_group_dir() / "Group.xlsx"

    group_dir: Path = get_group_dir()
    group_dir.mkdir(parents=True, exist_ok=True)
    return group_dir / f"{GROUP}{group_label}.xlsx"

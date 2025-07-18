from pathlib import Path

from pylms.constants import GROUP
from pylms.utils.paths.path_fns import get_paths_excel, get_excel_path


def get_group_path(group_label: int | None = None) -> Path:
    if group_label is None:
        return get_paths_excel()["Group"]
    else:
        group_dir: Path = get_excel_path() / "groups"
        group_dir.mkdir(parents=True, exist_ok=True)
        return group_dir / f"{GROUP}{group_label}.xlsx"

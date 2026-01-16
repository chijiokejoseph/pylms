import re
from pathlib import Path

from ..errors import Result, Unit, eprint
from ..info import print_info
from ..paths import get_excel_path
from .history import History


def set_group(history: History, num: int) -> Result[Unit]:
    group_path: Path = get_excel_path() / "groups"
    if not group_path.exists():
        msg = "Unable to set group field of History because no group path exists."
        eprint(msg)
        return Result.err(msg)

    items: list[Path] = list(group_path.iterdir())
    num_groups: int = len(
        [
            group
            for group in items
            if re.match(r"^Group\d+.xlsx$", group.name) is not None
        ]
    )
    print_info(f"Found {num_groups} groups\n")
    if num != num_groups:
        msg = "Unable to set group due to mismatch between the actual directory items in the path and the number specified"
        eprint(msg)
        return Result.err(msg)

    history.group = (True, num)
    return Result.unit()


def get_num_groups(history: History) -> int:
    """
    Returns the number of groups the students have been divided into.

    :return: (int) - The number of groups the students have been divided into.
    :rtype: int
    """

    return history.group[1]

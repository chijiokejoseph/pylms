from pathlib import Path

import polars as pl

from ..cli import input_bool, input_num
from ..constants import GROUP, NAME, SERIAL
from ..data import DataStore, write
from ..errors import Result, Unit, eprint
from ..history import History, set_group
from ..info import print_info
from ..paths import get_group_dir, get_group_path


def group(ds: DataStore, history: History) -> Result[Unit]:
    if len(history.recorded_update_forms) < len(history.update_forms):
        msg = "You need to record all of the update forms you created for the cohort before grouping students\n"
        eprint(msg)
        return Result.err(msg)

    groups_path: Path = get_group_path()
    group_dir: Path = get_group_dir()
    if groups_path.exists():
        print_info(
            f"You have already grouped students. \nPlease check the path {groups_path.resolve()} for the previous grouping operation you performed."
        )
        prompt: str = "Do you wish to update or redo the grouping?"

        result = input_bool(prompt)
        if result.is_err():
            return result.propagate()

        choice = result.unwrap()
        if not choice:
            return Result.unit()

    group_dir.mkdir(exist_ok=True)
    pretty = ds.pretty()

    msg: str = "Please enter the number of groups [Must be between 3 - 100]: "
    num_groups = input_num(msg, 1, lambda x: 3 <= x <= 100)

    if num_groups.is_err():
        return num_groups.propagate()

    num_groups = num_groups.unwrap()
    groups: list[int] = [
        num_groups if serial % num_groups == 0 else serial % num_groups
        for serial in range(1, pretty.height + 1)
    ]
    groups_df = pretty.select(pl.col(SERIAL), pl.col(NAME)).with_columns(
        pl.Series(GROUP, groups).alias(GROUP)
    )

    result = write(groups_df, groups_path)
    if result.is_err():
        return result.propagate()

    for group in range(1, num_groups + 1):
        group_df = groups_df.filter(pl.col(GROUP) == group)
        group_path: Path = get_group_path(group)

        result = write(group_df, group_path)
        if result.is_err():
            return result.propagate()

    return set_group(history, num_groups)

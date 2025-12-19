from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd

from ..cli import input_num, input_option
from ..constants import GROUP, NAME, SERIAL
from ..data import DataStore, DataStream
from ..errors import Result, Unit, eprint
from ..history import History, set_group
from ..paths import get_group_dir, get_group_path


def group(ds: DataStore, history: History) -> Result[Unit]:
    if len(history.recorded_update_forms) == 0 and len(history.update_forms) > 0:
        msg = "\nYou need to record at least one of the update forms you created for the cohort before grouping students\n"
        eprint(msg)
        return Result.err(msg)

    group_data_path: Path = get_group_path()
    group_dir: Path = get_group_dir()
    if group_data_path.exists():
        print(
            f"You have already grouped students. \nPlease check the path {group_data_path.resolve()} for the previous grouping operation you performed."
        )
        prompt: str = "Do you wish to update or redo the grouping?"
        options: list[str] = ["Yes", "No"]
        option_result = input_option(options, prompt=prompt)
        if option_result.is_err():
            return option_result.propagate()
        idx, _ = option_result.unwrap()
        if idx == 2:
            return Result.unit()

    group_dir.mkdir(exist_ok=True)
    pretty_data: pd.DataFrame = ds.pretty()

    msg: str = "Please enter the number of groups [Must be between 3 - 100]: "
    num_result = input_num(msg, 1, lambda x: 3 <= x <= 100)

    if num_result.is_err():
        return num_result.propagate()

    num_groups = num_result.unwrap()
    groups: list[int] = [
        num_groups if serial % num_groups == 0 else serial % num_groups
        for serial in range(1, pretty_data.shape[0] + 1)
    ]
    group_data: pd.DataFrame = pretty_data.loc[:, [SERIAL, NAME]]
    group_data[GROUP] = groups
    group_stream: DataStream[pd.DataFrame] = DataStream(group_data)
    group_stream.to_excel(group_data_path)
    groups_arr: np.ndarray = np.array(groups)

    for grp_num in range(1, num_groups + 1):
        mask: np.ndarray = cast(np.ndarray, groups_arr == grp_num)
        grp_num_data: pd.DataFrame = group_data.loc[mask, :]
        grp_num_stream: DataStream[pd.DataFrame] = DataStream(grp_num_data)
        grp_num_path: Path = get_group_path(grp_num)
        grp_num_stream.to_excel(grp_num_path)

    return set_group(history, num_groups)

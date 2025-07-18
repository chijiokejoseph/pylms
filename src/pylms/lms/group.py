from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd

from pylms.cli import input_num
from pylms.constants import GROUP, NAME, SERIAL
from pylms.utils import DataStore, DataStream, date, paths


def group(ds: DataStore) -> None:
    week_nums: tuple[int, ...] = date.to_unique_week_nums(date.retrieve_dates())
    penultimate_week: int = week_nums[-1]
    current_week: int = date.det_week_num()
    if current_week not in [penultimate_week - 1, penultimate_week]:
        print(
            "You can only group students at the penultimate week or the week preceding it.\n"
        )
        return None

    group_data_path: Path = paths.get_group_path()
    if group_data_path.exists():
        print(
            f"You have already grouped students. \nPlease check the path {group_data_path.resolve()} for the previous grouping operation you performed."
        )
        print(
            f"Should you need to update or redo the grouping, delete the old {group_data_path.name} file and then rerun the program.\n"
        )
        return None

    pretty_data: pd.DataFrame = ds.pretty()
    msg: str = "Please enter the number of groups [Must be between 3 - 10]: "
    temp: int | float = input_num(msg, "int", lambda x: 3 <= x <= 10)
    num_groups: int = cast(int, temp)
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
        grp_num_path: Path = paths.get_group_path(grp_num)
        grp_num_stream.to_excel(grp_num_path)

    return None

from datetime import datetime
from pathlib import Path
from typing import Any, Callable, cast
from uuid import UUID

import pandas as pd

from pylms.cache.cache import copy_data
from pylms.cli import input_num
from pylms.constants import CACHE_CMD, CACHE_ID, CACHE_TIME
from pylms.utils import DataStream, paths

type ValidatorFn = Callable[[pd.DataFrame | pd.Series], bool]


def verify_cache_records(test_data: pd.DataFrame) -> bool:
    cols: list[str] = test_data.columns.tolist()
    required_cols: list[str] = [CACHE_TIME, CACHE_CMD, CACHE_ID]
    return all(col in required_cols for col in cols)


def fmt_time(timestamp: str | datetime) -> str:
    if isinstance(timestamp, str):
        timestamp_date: datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    else:
        timestamp_date = timestamp
    return timestamp_date.strftime("%a, %d %b, %Y %I:%M%p")


def len_str(item: Any) -> int:
    return len(str(item))


def rollback_to_cmd(test_path: Path | None = None) -> None:
    cache_records: pd.DataFrame = pd.read_csv(str(paths.get_metadata_path()))
    validate_fn = cast(ValidatorFn, verify_cache_records)
    cache_stream: DataStream = DataStream(cache_records, validate_fn)
    cache_records = cache_stream()
    max_index_len: int = cache_records.shape[0]
    max_index_len = max(len_str(str(max_index_len)), len_str("Index"))
    max_time_len: int = max(
        [len_str(fmt_time(timestamp)) for timestamp in cache_records.loc[:, CACHE_TIME]]
    )
    max_time_len = max(max_time_len, len_str("Timestamp"))
    max_cmd_len: int = max([len_str(cmd) for cmd in cache_records.loc[:, CACHE_CMD]])
    max_cmd_len = max(max_cmd_len, len_str("Command"))
    print(
        f"{'Index':{max_index_len}}\t{'Timestamp':<{max_time_len}}\t{'Command':<{max_cmd_len}}\n"
    )
    for index, timestamp, cmd, _ in cache_records.itertuples():
        count = f"{index + 1}."
        print(
            f"{count:<{max_index_len}}\t{fmt_time(timestamp):<{max_time_len}}\t{cmd:<{max_cmd_len}}\n"
        )
    value: int | float = input_num(
        "Enter the index of the state to roll back to: ", "int"
    )
    idx: int = cast(int, value)
    snapshot_value = cache_records.loc[idx - 1, CACHE_ID]
    snapshot_id = UUID(cast(str, snapshot_value))
    snapshot_path = paths.get_snapshot_path(snapshot_id)
    if test_path is None:
        test_path = paths.get_data_path()
    copy_data(snapshot_id, snapshot_path, test_path)
    
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import polars as pl

from ..cli import input_num, print_data
from ..config import Config
from ..constants import CACHE_CMD, CACHE_ID, CACHE_TIME, COMMA_DELIM, SERIAL
from ..data import DataStream, read
from ..errors import Result, Unit
from ..info import print_info
from ..paths import get_data_path, get_metadata_path, get_snapshot_path
from .cache import copy_data


def verify_cache_records(test_data: pl.DataFrame) -> tuple[bool, str]:
    """Verify that the cache records DataFrame contains the required columns.

    Checks that the provided DataFrame contains the expected cache metadata
    columns: `CACHE_TIME`, `CACHE_CMD` and `CACHE_ID`.

    Args:
        test_data (pl.DataFrame): The DataFrame to verify.

    Returns:
        tuple[bool, str]: True if all required columns are present along with an empty string, False otherwise and a message indicating the invalid columns.
    """
    # Check if the required columns are present in the DataFrame
    cols = test_data.columns
    required_cols = [CACHE_TIME, CACHE_CMD, CACHE_ID]
    bad_cols = [col for col in cols if col not in required_cols]
    if len(bad_cols) > 0:
        columns = COMMA_DELIM.join(bad_cols)
        required_cols_print = COMMA_DELIM.join(required_cols)
        msg = f"columns: '{columns} are not part of the required_cols: '{required_cols_print}'"
        return False, msg
    return True, ""


def fmt_time(timestamp: str | datetime) -> str:
    """Format a timestamp into a readable string.

    Accepts either a timestamp string in the format '%Y-%m-%d %H:%M:%S' or a
    `datetime` object and returns a human-readable formatted string such as
    'Mon, 01 Jan, 2020 01:23PM'.

    Args:
        timestamp (str | datetime): The timestamp to format.

    Returns:
        str: The formatted timestamp string.
    """
    # If the timestamp is a string, parse it into a datetime object
    if isinstance(timestamp, str):
        timestamp_date: datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    else:
        # If the timestamp is already a datetime object, use it as is
        timestamp_date = timestamp
    # Format the datetime object into a readable string
    return timestamp_date.strftime("%a, %d %b, %Y %I:%M%p")


def len_str(item: Any) -> int:
    """Return the length of the string representation of an item.

    Args:
        item (Any): The object whose string representation length is required.

    Returns:
        int: Length of str(item).
    """
    return len(str(item))


def rollback_to_cmd(config: Config, test_path: Path | None = None) -> Result[Unit]:
    """Display cache records, prompt for a rollback selection, and perform the rollback operation.

    Args:
        config: Application configuration.
        test_path: Optional destination path to restore data to.

    Returns:
        Result[Unit]: Result object indicating success or a propagated error.
    """
    cache_records = read(get_metadata_path())
    if cache_records.is_err():
        return cache_records.propagate()

    cache_records = cache_records.unwrap()

    cache_stream = DataStream.new(cache_records, verify_cache_records)

    if cache_stream.is_err():
        return cache_stream.propagate()

    cache_stream = cache_stream.unwrap()
    cache_records = cache_stream.as_ref()
    cache_display = cache_records.with_columns(
        pl.int_range(1, cache_records.height+1).alias(SERIAL)
    ).select([SERIAL, CACHE_CMD, CACHE_ID])
    print_info("Cache Records are shown below\n")
    print_data(cache_display)

    # max_index_len: int = cache_records.shape[0]
    # max_index_len = max(len_str(str(max_index_len)), len_str("Index"))

    # max_time_len: int = max(
    #     [len_str(fmt_time(timestamp)) for timestamp in cache_records[CACHE_TIME]]
    # )
    # max_time_len = max(max_time_len, len_str("Timestamp"))

    # max_cmd_len: int = max([len_str(cmd) for cmd in cache_records[CACHE_CMD]])
    # max_cmd_len = max(max_cmd_len, len_str("Command"))

    # print(
    #     f"{'Index':{max_index_len}}\t{'Timestamp':<{max_time_len}}\t{'Command':<{max_cmd_len}}\n"
    # )

    # for count, row in enumerate(cache_records.to_arrow().to_pylist(), start=1):
    #     timestamp = row[CACHE_TIME]
    #     cmd = row[CACHE_CMD]
    #     print(
    #         f"{count:<{max_index_len}}\t{fmt_time(timestamp):<{max_time_len}}\t{cmd:<{max_cmd_len}}\n"
    #     )

    result = input_num(
        "Enter the index of the state to roll back to: ",
        1,
    )
    if result.is_err():
        return result.propagate()
    idx = result.unwrap()

    snapshot_value: str = cache_records.item(idx - 1, CACHE_ID)

    snapshot_id = UUID(snapshot_value)

    snapshot_path = get_snapshot_path(snapshot_id)

    if test_path is None:
        test_path = get_data_path(config)

    return copy_data(config, snapshot_id, snapshot_path, test_path)

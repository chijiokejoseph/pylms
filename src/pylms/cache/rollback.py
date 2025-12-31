from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import pandas as pd

from ..cli import input_num
from ..constants import CACHE_CMD, CACHE_ID, CACHE_TIME
from ..data import DataStream, read
from ..errors import Result, Unit
from ..paths import get_data_path, get_metadata_path, get_snapshot_path
from .cache import copy_data


def verify_cache_records(test_data: pd.DataFrame) -> bool:
    """Verify that the cache records DataFrame contains the required columns.

    Checks that the provided DataFrame contains the expected cache metadata
    columns: `CACHE_TIME`, `CACHE_CMD` and `CACHE_ID`.

    Args:
        test_data (pd.DataFrame): The DataFrame to verify.

    Returns:
        bool: True if all required columns are present, False otherwise.
    """
    # Check if the required columns are present in the DataFrame
    cols: list[str] = test_data.columns.tolist()
    required_cols: list[str] = [CACHE_TIME, CACHE_CMD, CACHE_ID]
    return all(col in required_cols for col in cols)


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


def rollback_to_cmd(test_path: Path | None = None) -> Result[Unit]:
    """Display cache records, prompt for a rollback selection, and perform the
    rollback operation by copying snapshot data to the target path.

    This function reads cache metadata, prints a formatted list of available
    snapshots, prompts the user to choose an index to restore, and then copies
    the selected snapshot into `test_path` (or the default data path). The
    function returns the `Result` produced by the copy operation.

    Args:
        test_path (Path | None): Optional destination path to restore data to.

    Returns:
        Result[Unit]: Result object indicating success or a propagated error.
    """
    # Read cache records from metadata path
    cache_records = read(get_metadata_path())
    if cache_records.is_err():
        return cache_records.propagate()

    cache_records = cache_records.unwrap()

    # Create a DataStream with validation
    cache_stream = DataStream(cache_records, verify_cache_records)

    # Validate and get the cache records
    cache_records = cache_stream()

    # Calculate max length for index column display
    max_index_len: int = cache_records.shape[0]
    max_index_len = max(len_str(str(max_index_len)), len_str("Index"))

    # Calculate max length for timestamp column display
    max_time_len: int = max(
        [len_str(fmt_time(timestamp)) for timestamp in cache_records.loc[:, CACHE_TIME]]
    )
    max_time_len = max(max_time_len, len_str("Timestamp"))

    # Calculate max length for command column display
    max_cmd_len: int = max([len_str(cmd) for cmd in cache_records.loc[:, CACHE_CMD]])
    max_cmd_len = max(max_cmd_len, len_str("Command"))

    # Print header row with column names
    print(
        f"{'Index':{max_index_len}}\t{'Timestamp':<{max_time_len}}\t{'Command':<{max_cmd_len}}\n"
    )

    # Iterate over cache records and print each with formatted values
    for index, timestamp, cmd, _ in cache_records.itertuples():
        count = f"{index + 1}."
        print(
            f"{count:<{max_index_len}}\t{fmt_time(timestamp):<{max_time_len}}\t{cmd:<{max_cmd_len}}\n"
        )

    # Prompt user to enter index for rollback
    result = input_num(
        "Enter the index of the state to roll back to: ",
        1,
    )
    if result.is_err():
        return result.propagate()
    idx = result.unwrap()

    # Get the snapshot ID from the selected cache record
    snapshot_value = cache_records[CACHE_ID].astype(str).iloc[idx - 1]
    snapshot_id = UUID(snapshot_value)

    # Get the snapshot path for the rollback
    snapshot_path = get_snapshot_path(snapshot_id)

    # Use provided test_path or default data path
    if test_path is None:
        test_path = get_data_path()

    # Perform the rollback by copying data from snapshot to test_path
    return copy_data(snapshot_id, snapshot_path, test_path)

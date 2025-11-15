from datetime import datetime
from pathlib import Path
from typing import Any, Callable, cast
from uuid import UUID

import pandas as pd

from pylms.cache.cache import copy_data
from pylms.cli import input_num
from pylms.constants import CACHE_CMD, CACHE_ID, CACHE_TIME
from pylms.errors import eprint
from pylms.utils import DataStream, paths

type ValidatorFn = Callable[[pd.DataFrame | pd.Series], bool]


def verify_cache_records(test_data: pd.DataFrame) -> bool:
    """
    Verify that the cache records DataFrame contains the required columns.

    :param test_data: (pd.DataFrame) - The DataFrame to verify.
    :type test_data: pd.DataFrame

    :return: (bool) - True if all required columns are present, False otherwise.
    :rtype: bool
    """
    # Check if the required columns are present in the DataFrame
    cols: list[str] = test_data.columns.tolist()
    required_cols: list[str] = [CACHE_TIME, CACHE_CMD, CACHE_ID]
    return all(col in required_cols for col in cols)


def fmt_time(timestamp: str | datetime) -> str:
    """
    Format a timestamp string or datetime object into a readable string format.

    :param timestamp: (str | datetime) - The timestamp to format.
    :type timestamp: str or datetime

    :return: (str) - The formatted timestamp string.
    :rtype: str
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
    """
    Get the length of the string representation of an item.

    :param item: (Any) - The item to measure.
    :type item: Any

    :return: (int) - The length of the string representation.
    :rtype: int
    """
    return len(str(item))


def rollback_to_cmd(test_path: Path | None = None) -> None:
    """
    Display cache records, prompt user to select a rollback state, and perform rollback.

    :param test_path: (Path | None) - Optional path to rollback data to.
    :type test_path: Path or None

    :return: (None) - returns None.
    :rtype: None
    """
    # Read cache records from metadata path
    cache_records: pd.DataFrame = pd.read_csv(str(paths.get_metadata_path()))

    # Cast the verify function to ValidatorFn type
    validate_fn = cast(ValidatorFn, verify_cache_records)

    # Create a DataStream with validation
    cache_stream: DataStream = DataStream(cache_records, validate_fn)

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
    value_result = input_num("Enter the index of the state to roll back to: ", "int")
    if value_result.is_err():
        eprint(f"Error retrieving index: {value_result.unwrap_err()}")
        return None
    value = value_result.unwrap()
    idx: int = cast(int, value)

    # Get the snapshot ID from the selected cache record
    snapshot_value = cache_records.loc[idx - 1, CACHE_ID]
    snapshot_id = UUID(cast(str, snapshot_value))

    # Get the snapshot path for the rollback
    snapshot_path = paths.get_snapshot_path(snapshot_id)

    # Use provided test_path or default data path
    if test_path is None:
        test_path = paths.get_data_path()

    # Perform the rollback by copying data from snapshot to test_path
    copy_data(snapshot_id, snapshot_path, test_path)

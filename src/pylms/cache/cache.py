import shutil
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

import pandas as pd

from ..constants import CACHE_CMD, CACHE_ID, CACHE_TIME
from ..data import read
from ..errors import Result, Unit, eprint
from ..paths import (
    get_cache_path,
    get_data_path,
    get_metadata_path,
    get_snapshot_path,
    rm_path,
)


def new_cache_record(command: str) -> tuple[pd.DataFrame, UUID]:
    """
    Create a new cache record with the given command and generate a unique snapshot ID.

    :param command: (str) - The command description to be cached.
    :type command: str

    :return: (tuple[pd.DataFrame, UUID]) - A tuple containing the cache record DataFrame and the snapshot UUID.
    :rtype: tuple[pd.DataFrame, UUID]
    """
    # Get the current datetime
    now: datetime = datetime.now()
    # Format the datetime as a string
    timestamp: str = now.strftime("%Y-%m-%d %H:%M:%S")
    # Generate a new unique snapshot ID
    snapshot: UUID = uuid4()
    # Create and return the cache record DataFrame and snapshot ID
    return pd.DataFrame(
        data={
            CACHE_TIME: [timestamp],
            CACHE_CMD: [command],
            CACHE_ID: [snapshot],
        }
    ), snapshot


def copy_dir(src_dir: Path, dst_dir: Path) -> Result[Unit]:
    """
    Recursively copy the contents of the source directory to the destination directory.

    :param src_dir: (Path) - The source directory path.
    :param dst_dir: (Path) - The destination directory path.

    :return: a result object
    :rtype: Result[Unit]
    """
    # Return early if source directory does not exist
    if not src_dir.is_dir():
        msg = f"src path: '{src_dir:<20}' does not exist"
        eprint(msg)
        return Result.err(FileNotFoundError(msg))
    # Iterate over items in the source directory
    for item in src_dir.iterdir():
        new_item: Path = dst_dir / item.name
        # Recursively copy directories
        if item.is_dir():
            result = copy_dir(item, new_item)
            if result.is_err():
                return result.propagate()
        else:
            # Copy files
            _ = shutil.copy2(item, new_item)
    return Result.unit()


def copy_data(
    snapshot_id: UUID,
    src: Path | None = None,
    dst: Path | None = None,
) -> Result[Unit]:
    """
    Copy data from source to destination paths with error handling for permissions and shutil errors. It copies from source to destination paths, excluding cache directory.

    :param snapshot_id: (UUID) - The unique snapshot identifier.
    :param src_path: (Path | None) - Optional source path to copy from.
    :param dst_path: (Path | None) - Optional destination path to copy to.

    :return: (Result[Unit]) - returns a result object
    :rtype: Result[Unit]
    """
    # Determine source and destination paths if not provided
    if src is None or dst is None:
        # Use default paths if not provided
        new_path: Path = get_snapshot_path(snapshot_id)
        new_path.mkdir(parents=True, exist_ok=True)
        src = get_data_path()
        dst = new_path

    # Remove existing items in destination except cache directory
    for item in dst.iterdir():
        # Skip cache directory
        if item.name == get_cache_path().name:
            continue
        # Remove items
        result = rm_path(item)
        if result.is_err():
            return result.propagate()

    # Copy items from source to destination, excluding cache directory
    for item in src.iterdir():
        # Skip cache directory
        if item.name == get_cache_path().name:
            continue
        # Recursively copy directories
        new_item: Path = dst / item.name

        try:
            # Check if item is a directory
            if item.is_dir():
                # Recursively copy directory
                _ = shutil.copytree(item, new_item, dirs_exist_ok=True)
            else:
                # Copy file
                _ = shutil.copy2(item, new_item)
        except PermissionError as e:
            # Handle permission errors
            msg = f"Failed to copy item: '{item.name}' from src: '{src}' to dst: '{dst}'.\nError: {e}"
            eprint(msg)
            return Result.err(e)
        except shutil.Error as e:
            # Handle shutil errors
            msg = f"Failed to copy item: '{item.name}' from src: '{src}' to dst: '{dst}'.\nError: {e}"
            eprint(msg)
            return Result.err(msg)

    return Result.unit()


def cache_for_cmd(cmd: str) -> Result[Unit]:
    """
    Cache the given command by creating a new cache record and copying data.

    :param cmd: (str) - The command description to cache.

    :return: (Result[Unit]) - returns result
    :rtype: Result[Unit]
    """
    # Create a new cache record and get the snapshot ID
    record, snapshot_id = new_cache_record(cmd)

    # Copy data to the snapshot location
    result = copy_data(snapshot_id)
    if result.is_err():
        return result

    # Check if metadata path exists to update or create cache metadata
    if get_metadata_path().exists():
        cache = read(get_metadata_path())

        if cache.is_err():
            return cache.propagate()

        cache = cache.unwrap()

        # Limit cache size by trimming older records if necessary
        if cache.shape[0] >= 100:
            cache = cache.loc[50:, :]

        # Append new record to cache
        cache = pd.concat((cache, record), axis=0)

        # Save updated cache metadata
        cache.to_csv(get_metadata_path(), index=False)
    else:
        # Create new cache metadata file
        record.to_csv(get_metadata_path(), index=False)

    return Result.unit()

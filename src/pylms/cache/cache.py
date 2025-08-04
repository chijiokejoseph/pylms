import shutil
from datetime import datetime
from pathlib import Path
from typing import cast
from uuid import UUID, uuid4

import pandas as pd

from pylms.constants import CACHE_CMD, CACHE_ID, CACHE_TIME
from pylms.utils import paths, read_csv, rm_path
from pylms.cache.errors import FilePermissionError, ShutilOpsError


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


def copy_dir(src_dir: Path, dst_dir: Path) -> None:
    """
    Recursively copy the contents of the source directory to the destination directory.

    :param src_dir: (Path) - The source directory path.
    :param dst_dir: (Path) - The destination directory path.

    :return: None
    :rtype: None
    """
    # Return early if source directory does not exist
    if not src_dir.is_dir():
        return None
    # Iterate over items in the source directory
    for item in src_dir.iterdir():
        new_item: Path = dst_dir / item.name
        # Recursively copy directories
        if item.is_dir():
            copy_dir(item, new_item)
        else:
            # Copy files
            shutil.copy2(item, new_item)
    return None


def _copy_data(
    snapshot_id: UUID,
    src_path: Path | None = None,
    dst_path: Path | None = None,
) -> None:
    """
    Internal function to copy data from source to destination paths, excluding cache directory.

    :param snapshot_id: (UUID) - The unique snapshot identifier.
    :param src_path: (Path | None) - Optional source path to copy from.
    :param dst_path: (Path | None) - Optional destination path to copy to.

    :return: (None) - returns None
    :rtype: None
    """
    # Determine source and destination paths if not provided
    if src_path is None and dst_path is None:
        # Use default paths if not provided
        new_path: Path = paths.get_snapshot_path(snapshot_id)
        new_path.mkdir(parents=True, exist_ok=True)
        src: Path = paths.get_data_path()
        dst: Path = new_path
    else:
        # Use provided paths if available
        src = cast(Path, src_path)
        dst = cast(Path, dst_path)

    # Remove existing items in destination except cache directory
    for item in dst.iterdir():
        # Skip cache directory
        if item.name == paths.get_cache_path().name:
            continue
        # Remove items
        rm_path(item)
        
    # Copy items from source to destination, excluding cache directory
    for item in src.iterdir():
        # Skip cache directory
        if item.name == paths.get_cache_path().name:
            continue
        # Recursively copy directories
        new_item: Path = dst / item.name
        # Check if item is a directory
        if item.is_dir():
            # Recursively copy directory
            shutil.copytree(item, new_item, dirs_exist_ok=True)
        else:
            # Copy file
            shutil.copy2(item, new_item)
            
def copy_data(
    snapshot_id: UUID,
    src_path: Path | None = None,
    dst_path: Path | None = None,
) -> None:
    """
    Copy data from source to destination paths with error handling for permissions and shutil errors.

    :param snapshot_id: (UUID) - The unique snapshot identifier.
    :param src_path: (Path | None) - Optional source path to copy from.
    :param dst_path: (Path | None) - Optional destination path to copy to.

    :return: (None) - returns None
    :rtype: None
    """
    try:
        # Copy data from source to destination
        _copy_data(snapshot_id, src_path, dst_path)
    except PermissionError as e:
        # Handle permission errors
        raise FilePermissionError(str(e))
    except shutil.Error as e:
        # Handle shutil errors
        raise ShutilOpsError(str(e))


def cache_for_cmd(cmd: str) -> None:
    """
    Cache the given command by creating a new cache record and copying data.

    :param cmd: (str) - The command description to cache.

    :return: (None) - returns None
    :rtype: None
    """
    # Create a new cache record and get the snapshot ID
    record, snapshot_id = new_cache_record(cmd)
    
    # Copy data to the snapshot location
    copy_data(snapshot_id)
    
    # Check if metadata path exists to update or create cache metadata
    if paths.get_metadata_path().exists():
        cache: pd.DataFrame = read_csv(paths.get_metadata_path())
        
        # Limit cache size by trimming older records if necessary
        if cache.shape[0] >= 100:
            cache = cache.loc[50:, :]
            
        # Append new record to cache
        cache = pd.concat((cache, record), axis=0)
        
        # Save updated cache metadata
        cache.to_csv(paths.get_metadata_path(), index=False)
    else:
        # Create new cache metadata file
        record.to_csv(paths.get_metadata_path(), index=False)

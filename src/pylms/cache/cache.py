import shutil
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

import polars as pl

from ..constants import CACHE_CMD, CACHE_ID, CACHE_TIME
from ..config import Config
from ..data import read, write
from ..errors import Result, Unit, eprint
from ..paths import (
    get_cache_path,
    get_metadata_path,
    get_snapshot_path,
    get_data_path,
    rm_path,
)


def new_cache_record(command: str) -> tuple[pl.DataFrame, UUID]:
    """Create a new cache record and generate a snapshot UUID.

    Create a one-row DataFrame containing cache metadata (timestamp, command,
    snapshot UUID) and return that DataFrame together with the generated
    UUID. The timestamp is formatted as "%Y-%m-%d %H:%M:%S".

    Args:
        command (str): Description of the command or operation to cache.

    Returns:
        tuple[pl.DataFrame, UUID]: A DataFrame containing the new cache record
            and the generated snapshot UUID.
    """
    # Get the current datetime
    now: datetime = datetime.now()
    # Format the datetime as a string
    timestamp: str = now.strftime("%Y-%m-%d %H:%M:%S")
    # Generate a new unique snapshot ID
    snapshot: UUID = uuid4()
    # Create and return the cache record DataFrame and snapshot ID
    return pl.DataFrame(
        data={
            CACHE_TIME: [timestamp],
            CACHE_CMD: [command],
            CACHE_ID: [str(snapshot)],
        }
    ), snapshot


def copy_dir(src_dir: Path, dst_dir: Path) -> Result[Unit]:
    """Recursively copy the contents of a source directory to a destination.

    Recursively copy all files and subdirectories from `src_dir` into
    `dst_dir`. If `src_dir` does not exist a `Result.err` is returned. The
    function preserves the directory tree by recursing into subdirectories.

    Args:
        src_dir (Path): Source directory path.
        dst_dir (Path): Destination directory path.

    Returns:
        Result[Unit]: Ok on success or Err with the underlying error.
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
    config: Config,
    snapshot_id: UUID,
    src: Path | None = None,
    dst: Path | None = None,
) -> Result[Unit]:
    """Copy project data into a snapshot or restore from a snapshot.

    Args:
        snapshot_id: Identifier for the snapshot.
        src: Optional source path. When None, the current data path is used.
        dst: Optional destination path. When None, a snapshot directory for snapshot_id is created and used.

    Returns:
        Result[Unit]: Ok on success or Err containing the encountered error.
    """
    if src is None or dst is None:
        new_path: Path = get_snapshot_path(snapshot_id)
        new_path.mkdir(parents=True, exist_ok=True)
        src = get_data_path(config)
        dst = new_path

    cache_path_name = get_cache_path().name

    for item in dst.iterdir():
        if item.name == cache_path_name:
            continue
        result = rm_path(item)
        if result.is_err():
            return result.propagate()

    for item in src.iterdir():
        if item.name == cache_path_name:
            continue
        new_item: Path = dst / item.name

        try:
            if item.is_dir():
                _ = shutil.copytree(item, new_item, dirs_exist_ok=True)
            else:
                _ = shutil.copy2(item, new_item)
        except PermissionError as e:
            msg = f"Failed to copy item: '{item.name}' from src: '{src}' to dst: '{dst}'.\nError: {e}"
            eprint(msg)
            return Result.err(e)
        except shutil.Error as e:
            msg = f"Failed to copy item: '{item.name}' from src: '{src}' to dst: '{dst}'.\nError: {e}"
            eprint(msg)
            return Result.err(msg)

    return Result.unit()


def cache_for_cmd(config: Config, cmd: str) -> Result[Unit]:
    """Create a cache snapshot for a command and update metadata.

    Args:
        cmd: Description of the command being cached.

    Returns:
        Result[Unit]: Ok on success or Err containing the error encountered.
    """
    record, snapshot_id = new_cache_record(cmd)

    result = copy_data(config, snapshot_id)
    if result.is_err():
        return result

    metadata_path = get_metadata_path()
    if metadata_path.exists():
        cache = read(metadata_path)

        if cache.is_err():
            return cache.propagate()

        cache = cache.unwrap()

        if cache.height >= 100:
            cache = cache[50:]

        cache = cache.vstack(record)

        return write(cache, metadata_path)
    else:
        return write(record, metadata_path)

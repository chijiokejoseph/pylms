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
    now: datetime = datetime.now()
    timestamp: str = now.strftime("%Y-%m-%d %H:%M:%S")
    snapshot: UUID = uuid4()
    return pd.DataFrame(
        data={
            CACHE_TIME: [timestamp],
            CACHE_CMD: [command],
            CACHE_ID: [snapshot],
        }
    ), snapshot


def copy_dir(src_dir: Path, dst_dir: Path) -> None:
    if not src_dir.is_dir():
        return None
    for item in src_dir.iterdir():
        new_item: Path = dst_dir / item.name
        if item.is_dir():
            copy_dir(item, new_item)
        else:
            shutil.copy2(item, new_item)
    return None


def _copy_data(
    snapshot_id: UUID,
    src_path: Path | None = None,
    dst_path: Path | None = None,
) -> None:
    if src_path is None and dst_path is None:
        new_path: Path = paths.get_snapshot_path(snapshot_id)
        new_path.mkdir(parents=True, exist_ok=True)
        src: Path = paths.get_data_path()
        dst: Path = new_path
    else:
        src = cast(Path, src_path)
        dst = cast(Path, dst_path)

    for item in dst.iterdir():
        if item.name == paths.get_cache_path().name:
            continue
        rm_path(item)
    for item in src.iterdir():
        if item.name == paths.get_cache_path().name:
            continue
        new_item: Path = dst / item.name
        if item.is_dir():
            shutil.copytree(item, new_item, dirs_exist_ok=True)
        else:
            shutil.copy2(item, new_item)
            
def copy_data(
    snapshot_id: UUID,
    src_path: Path | None = None,
    dst_path: Path | None = None,
) -> None:
    try:
        _copy_data(snapshot_id, src_path, dst_path)
    except PermissionError as e:
        raise FilePermissionError(str(e))
    except shutil.Error as e:
        raise ShutilOpsError(str(e))


def cache_for_cmd(cmd: str) -> None:
    record, snapshot_id = new_cache_record(cmd)
    copy_data(snapshot_id)
    if paths.get_metadata_path().exists():
        cache: pd.DataFrame = read_csv(paths.get_metadata_path())
        if cache.shape[0] >= 100:
            cache = cache.loc[50:, :]
        cache = pd.concat((cache, record), axis=0)
        cache.to_csv(paths.get_metadata_path(), index=False)
    else:
        record.to_csv(paths.get_metadata_path(), index=False)


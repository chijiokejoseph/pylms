from pathlib import Path
from uuid import UUID

from ..constants import DATA_PATH


def get_cache_path() -> Path:
    return DATA_PATH / ".cache"


def get_snapshot_path(snapshot_id: UUID) -> Path:
    return get_cache_path() / f"Snapshot{snapshot_id}"


def get_metadata_path() -> Path:
    return get_cache_path() / "Metadata.csv"

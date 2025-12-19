from pathlib import Path
from uuid import UUID

from .path_fns import get_cache_path, get_data_path


def get_snapshot_path(snapshot_id: UUID) -> Path:
    return get_data_path() / ".cache" / f"Snapshot{snapshot_id}"


def get_metadata_path() -> Path:
    return get_cache_path() / "Metadata.csv"

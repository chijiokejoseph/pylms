from uuid import UUID
from pathlib import Path

from pylms.utils.paths.path_fns import get_cache_path
from pylms.utils.paths.path_fns import get_data_path


def get_snapshot_path(snapshot_id: UUID) -> Path:
    return get_data_path() / ".cache" / f"Snapshot{snapshot_id}"


def get_metadata_path() -> Path:
    return get_cache_path() / "Metadata.csv"
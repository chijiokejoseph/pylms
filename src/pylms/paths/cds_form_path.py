from pathlib import Path
from typing import Literal

from .path_fns import get_paths_json


def get_cds_path(path_type: Literal["form", "record"], timestamp: str) -> Path:
    if path_type == "form":
        return get_paths_json()["CDS"] / f"{timestamp}_cds_form.json"
    else:
        return get_paths_json()["CDS"] / f"{timestamp}_cds_record.json"

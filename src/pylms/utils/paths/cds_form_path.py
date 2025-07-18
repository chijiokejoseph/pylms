from typing import Literal
from pathlib import Path
from pylms.utils.paths.path_fns import get_paths_json


def get_cds_path(path_type: Literal["form", "record"]) -> Path:
    if path_type == "form":
        return get_paths_json()["CDSForm"]
    else:
        return get_paths_json()["CDSRecord"]
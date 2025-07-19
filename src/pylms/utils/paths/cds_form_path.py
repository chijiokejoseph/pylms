from typing import Literal
from pathlib import Path
from pylms.utils.paths.path_fns import get_paths_json


def get_cds_path(path_type: Literal["form", "record"], uuid: str) -> Path:
    if path_type == "form":
        return get_paths_json()["CDSForm"] / f"_{uuid}.json"
    else:
        return get_paths_json()["CDSRecord"] / f"_{uuid}.json"

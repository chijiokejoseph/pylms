import os
from pathlib import Path

from ..errors import Result, Unit, eprint


def rm_path(path: Path, must_exist: bool = False) -> Result[Unit]:
    try:
        if not path.exists() and must_exist:
            msg = f"path: '{path}' was not found"
            eprint(msg)
            return Result.err(msg)
        if not path.exists():
            return Result.unit()
        if not path.is_dir():
            os.remove(path)
            return Result.unit()
        for item in path.iterdir():
            return rm_path(item, must_exist=False)
    except RecursionError:
        msg = f"Unable to completely delete path = {path}. Please delete the rest manually."
        eprint(msg)
        return Result.err(msg)
    return Result.unit()

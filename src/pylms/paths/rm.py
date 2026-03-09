import shutil
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
        shutil.rmtree(path)
    except RecursionError:
        msg = f"Unable to completely delete path = {path}. Please delete the rest manually."
        eprint(msg)
        return Result.err(msg)
    except PermissionError:
        msg = f"Unable to delete path = {path} due to permission error. Please delete it manually."
        eprint(msg)
        return Result.err(msg)
    except shutil.Error:
        msg = f"Unable to delete path = {path} due to an error. Please delete it manually."
        eprint(msg)
        return Result.err(msg)
    return Result.unit()

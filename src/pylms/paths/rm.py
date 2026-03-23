import os
import shutil
import stat
import time
from pathlib import Path

from ..errors import Result, Unit, eprint


def handle_readonly(func, path, exec_info) -> None:  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType, reportUnusedParameter]
    os.chmod(path, stat.S_IWRITE)
    func(path)


def rm_path(
    path: Path, must_exist: bool = False, delay: float = 0.5, retries: int = 5
) -> Result[Unit]:
    error: Exception | None = None
    while True:
        if retries == 0:
            break
        try:
            if not path.exists() and must_exist:
                msg = f"path: '{path}' was not found"
                eprint(msg)
                return Result.err(msg)
            if not path.exists():
                return Result.unit()
            if path.is_dir():
                shutil.rmtree(path, onexc=handle_readonly)
            else:
                os.chmod(path, stat.S_IWRITE)
                os.remove(path)
        except Exception as e:
            error = e
            time.sleep(delay)
            retries -= 1
            continue

    if isinstance(error, RecursionError):
        msg = f"Unable to completely delete path = {path}. Please delete the rest manually."
        eprint(msg)
        return Result.err(msg)
    elif isinstance(error, PermissionError):
        msg = f"Unable to delete path = {path} due to permission error. Please delete it manually."
        eprint(msg)
        return Result.err(msg)
    elif isinstance(error, shutil.Error):
        msg = f"Unable to delete path = {path} due to an error. Please delete it manually."
        eprint(msg)
        return Result.err(msg)
    else:
        return Result.unit()

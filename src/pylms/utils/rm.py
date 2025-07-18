import os
from pathlib import Path

from pylms.errors import LMSError


class PathNotFoundError(LMSError):
    def __init__(self, path: Path) -> None:
        self.message = f"Path '{path}' does not exist"
        super().__init__(self.message)


def rm_path(path: Path, must_exist: bool = True) -> None:
    try:
        if not path.exists() and must_exist:
            raise PathNotFoundError(path)
        if not path.exists():
            return None
        if not path.is_dir():
            os.remove(path)
            return None
        for item in path.iterdir():
            rm_path(item, must_exist=False)
    except RecursionError:
        print(
            f"Unable to completely delete path = {path}. Please delete the rest manually."
        )
    return None
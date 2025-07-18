from pathlib import Path
from typing import Callable

import pandas as pd

from pylms.utils.data.errors import ReadError


def read(path: Path) -> pd.DataFrame:
    return pd.read_excel(str(path))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(str(path))


def read_na(path: Path) -> pd.DataFrame:
    return pd.read_excel(str(path), keep_default_na=False)


def read_data(path: Path, keep_na: bool = False) -> pd.DataFrame:
    read_fn: Callable[[Path], pd.DataFrame] = read_na if keep_na else read
    try:
        data: pd.DataFrame = read_fn(path)
        return data
    except FileNotFoundError as e:
        raise ReadError(
            "FileNotFoundError",
            f"Please the path {path} has not been found. Error Details: {e}",
        )
    except PermissionError as e:
        raise ReadError(
            "PermissionError",
            f"Data at path {path} is in use by anther program or process. Error Details: {e}",
        )

from pathlib import Path

import pandas as pd

from ..errors import LMSError, Result, eprint


def read(path: Path, keep_na: bool = False) -> Result[pd.DataFrame]:
    if not path.exists():
        msg = f"path: '{path} not found"
        eprint(msg)
        return Result.err(FileNotFoundError(msg))

    try:
        if path.name.endswith("xlsx"):
            data = pd.read_excel(path, keep_default_na=keep_na)  # pyright: ignore [reportUnknownMemberType]
        elif path.name.endswith("csv"):
            data = pd.read_csv(path, keep_default_na=keep_na)  # pyright: ignore [reportUnknownMemberType]
        else:
            msg = f"file: '{path.name}' contains an unsupported file format. Only excel and csv files are supported"
            eprint(msg)
            return Result.err(LMSError(msg))

        return Result.ok(data)
    except PermissionError as e:
        msg = f"path: '{path}' is in use by another process"
        eprint(msg)
        return Result.err(e)
    except pd.errors.EmptyDataError as e:
        msg = f"path: '{path}' contains empty headers"
        eprint(msg)
        return Result.err(e)

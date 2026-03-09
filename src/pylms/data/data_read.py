from pathlib import Path

import polars as pl

from ..errors import Result, eprint


def read(path: Path, raw: bool = False) -> Result[pl.DataFrame]:
    """Read a tabular file (Excel or CSV) into a pandas DataFrame.

    Attempts to read the file located at `path` as either an Excel (.xlsx)
    workbook or a CSV (.csv) file and returns a `Result` containing the
    parsed `pandas.DataFrame` on success. Errors encountered while locating,
    reading, or parsing the file are wrapped in a failed `Result`.

    Args:
        path (Path): Path to the input file to read.

    Returns:
        Result[pl.DataFrame]: `Result.ok(DataFrame)` when reading succeeds;
            otherwise `Result.err(exception)` where the exception describes the failure.

    Catches:
        FileNotFoundError: If `path` does not exist (reported via `Result.err`).
        LMSError: If the file extension is unsupported (reported via `Result.err`).
        PermissionError: If the file cannot be accessed because it is in use
            by another process (reported via `Result.err`).
        pandas.errors.EmptyDataError: If the file contains empty headers
            or otherwise cannot be parsed as tabular data (reported via `Result.err`).

    Examples:
        >>> read(Path('students.xlsx'))
        Result.ok(<DataFrame ...>)
    """
    # Early-exit if the provided path does not exist to avoid attempting I/O.
    if not path.exists():
        msg = f"path: '{path} not found"
        eprint(msg)
        return Result.err(msg)

    try:
        # choose the appropriate polars method based on the file type
        if path.name.endswith("xlsx"):
            data = pl.read_excel(path, has_header=True) if not raw else pl.read_excel(path, has_header=True, infer_schema_length=0)
        elif path.name.endswith("csv"):
            data = pl.scan_csv(path, has_header=True).collect() if not raw else pl.read_csv(path, has_header=True, infer_schema=False)
        elif path.name.endswith("parquet"):
            data = pl.scan_parquet(path).collect()
        else:
            # Unsupported extension — log a clear message and return a domain error.
            msg = f"file: '{path.name}' contains an unsupported file format. Only excel and csv files are supported"
            eprint(msg)
            return Result.err(msg)

        # Successful read — return the DataFrame wrapped in a success Result.
        return Result.ok(data)
    except PermissionError:
        # PermissionError commonly indicates the file is locked by another process.
        # Log the condition and propagate it inside a failed Result so callers can
        # handle retries or user prompts.
        msg = f"path: '{path}' is in use by another process"
        eprint(msg)
        return Result.err(msg)

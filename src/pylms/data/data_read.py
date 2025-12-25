from pathlib import Path

import pandas as pd

from ..errors import Result, eprint


def read(path: Path, keep_na: bool = False) -> Result[pd.DataFrame]:
    """Read a tabular file (Excel or CSV) into a pandas DataFrame.

    Attempts to read the file located at `path` as either an Excel (.xlsx)
    workbook or a CSV (.csv) file and returns a `Result` containing the
    parsed `pandas.DataFrame` on success. Errors encountered while locating,
    reading, or parsing the file are wrapped in a failed `Result`.

    Args:
        path (Path): Path to the input file to read.
        keep_na (bool): If True, preserve pandas' default NA handling when
            reading (passed to pandas via `keep_default_na`). Defaults to False.

    Returns:
        Result[pd.DataFrame]: `Result.ok(DataFrame)` when reading succeeds;
            otherwise `Result.err(exception)` where the exception describes the failure.

    Raises:
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
        # Choose the appropriate pandas reader based on file extension.
        # We prefer explicit extension checks to avoid relying on pandas'
        # automatic engine selection, which can lead to surprising behavior.
        if path.name.endswith("xlsx"):
            # Read Excel workbook. `keep_default_na` controls NA parsing behavior.
            # The pyright ignore is present because pandas types are not fully
            # recognized by the static checker in this project.
            data = pd.read_excel(path, keep_default_na=keep_na)  # pyright: ignore [reportUnknownMemberType]
        elif path.name.endswith("csv"):
            # Read CSV file. Keep same `keep_na` semantics.
            data = pd.read_csv(path, keep_default_na=keep_na)  # pyright: ignore [reportUnknownMemberType]
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
    except pd.errors.EmptyDataError:
        # pandas raises EmptyDataError when a file has no content or malformed headers.
        # We surface that as a failed Result so higher-level code can present a user-friendly message.
        msg = f"path: '{path}' contains empty headers"
        eprint(msg)
        return Result.err(msg)

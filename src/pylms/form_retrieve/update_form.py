import re

import polars as pl

from ..data import DataStream
from ..errors import Result
from ..form_utils import UpdateFormInfo, select_form
from ..history import History
from .form import retrieve_form


def _rename_date_col(col: str) -> str:
    """Extract date from column name if it starts with 'Class'.
    
    Args:
        col (str): Column name to process.
        
    Returns:
        str: Extracted date in MM/DD/YYYY format or original column name.
    """
    if col.startswith("Class"):
        date_match: re.Match[str] | None = re.search(r"\d{2}/\d{2}/\d{4}", col)
        if date_match is not None:
            return date_match.group()
        return col
    return col


def rename_date_col(data_stream: DataStream) -> DataStream:
    """Rename date columns by extracting dates from class column names.
    
    Args:
        data_stream (DataStream): Input data stream.
        
    Returns:
        DataStream: Data stream with renamed date columns.
    """
    data = data_stream.as_ref()
    for column in data.columns:
        new_column = _rename_date_col(column)
        if new_column != column:
            data = data.with_columns(pl.col(column).alias(new_column))

    return DataStream(data)


def retrieve_update_form(
    history: History,
) -> Result[tuple[DataStream, UpdateFormInfo]]:
    """Retrieve update form data from history.
    
    Args:
        history (History): History object containing form information.
        
    Returns:
        Result[tuple[DataStream, UpdateFormInfo]]: Success with form data and info or error.
    """
    info = select_form(history, "update")
    if info.is_err():
        return info.propagate()

    info = info.unwrap()

    # Retrieve form data
    result = retrieve_form(info)
    if result.is_err():
        return result.propagate()
    result = result.unwrap()

    # Rename date columns for consistency
    result = rename_date_col(result)
    return Result.ok((result, info))

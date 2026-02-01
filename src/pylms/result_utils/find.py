import re
from typing import Literal


from ..constants import REQ
from ..data import DataStream
from ..errors import Result, eprint


def find_col(
    stream: DataStream,
    col_name: Literal["Assessment", "Attendance", "Project", "Result"],
    col_type: Literal["Score", "Count", "Req"],
) -> Result[str]:
    """Find column name based on type and category.
    
    Locates specific column types (Score, Count, Req) for given categories
    (Assessment, Attendance, Project, Result) in the data stream.
    
    Args:
        stream (DataStream): DataStream containing columns to search.
        col_name (Literal): Column category to search for.
        col_type (Literal): Type of column within category.
        
    Returns:
        Result[str]: Success with found column name or error.
        
    Note:
        - Only "Attendance" supports "Count" type
        - "Project" does not support "Req" type
    """
    result_data = stream.as_ref()
    column = col_name
    target_cols = [
        col for col in result_data.columns if col.startswith(column)
    ]
    if len(target_cols) == 0:
        msg = f"Expected some cols with the name '{column}'"
        eprint(msg)
        return Result.err(msg)

    match col_type:
        case "Score":
            target_cols = [
                col
                for col in target_cols
                if col.find(REQ) == -1 and col.find("%") != -1
            ]
        case "Count":
            if col_name != "Attendance":
                msg = "Cannot call the function with `col_name` not set to 'Attendance' and `col_type` set to 'Count'."
                eprint(msg)
                return Result.err(msg)
            target_cols = [
                col
                for col in target_cols
                if col.find(REQ) == -1 and col.find("%") == -1
            ]
        case "Req":
            if col_name == "Project":
                msg = "Cannot call the function with `col_name` set to 'Project' and `col_type` set to 'Req'."
                eprint(msg)
                return Result.err(msg)
            target_cols = [
                col
                for col in target_cols
                if col.find(REQ) != -1 and col.find("%") == -1
            ]

    if len(target_cols) == 0:
        msg = f"Expected at least 1 col with name '{col_name}' but without the name '{REQ}'"
        eprint(msg)
        return Result.err(msg)
    return Result.ok(target_cols[0])


def find_count(col_name: str) -> int | None:
    """Extract numeric count from column name.
    
    Searches for first numeric value in column name string.
    
    Args:
        col_name (str): Column name to search for numeric count.
        
    Returns:
        int | None: Extracted count or None if no number found.
    """
    item = re.search(r"(\d+)", col_name)
    if item is None:
        return None
    item_str = item.group(0)
    return int(item_str)

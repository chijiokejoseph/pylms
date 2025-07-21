import re
import pandas as pd
from typing import Literal

from pylms.constants import REQ
from pylms.lms.collate.errors import SpreadSheetFmtErr
from pylms.lms.utils.errors import BadArgumentErr
from pylms.utils import DataStream


def find_col(
    stream: DataStream[pd.DataFrame],
    col_name: Literal["Assessment", "Attendance", "Project", "Result"],
    col_type: Literal["Score", "Count", "Req"],
) -> str:
    """
    locates an "Assessment", "Attendance" or "Project" column based on the `col_name` argument, which is either a "Score", "Count", or "Req" column. At the last modification of this API, Only "Attendance" has a "Count" column, and only "Project" does not have a "Req" column.

    Hence, specifying "Project" as the `col_name` argument alongside "Req" as the `col_type` argument raises an error. Moreover, specifying any other column asides "Attendance" as `col_name` with the `col_type` set to "Count" raises an error.

    :param stream: (DataStream) - DataStream containing the columns on which the search is being made. This is a DataStream containing the results of students' data which has been generated during collation.
    :type stream: DataStream

    :param col_name: (Literal["Assessment", "Attendance", "Project", "Result"]) - "Assessment", "Attendance", "Project", "Result", literals indicating the main name of the column being searched for.
    :type col_name: (Literal["Assessment", "Attendance", "Project"])

    :param col_type: (Literal["Score", "Count", "Req"]) - "Score", "Count" or "Req" literals which indicate whether the columns to retrieve are score values like 75%, attendance counts, like 11 out of 12 or Cutoff / Requirement cols.
    :return: (str) - a string containing the name of the column which is being searched for.
    """
    result_data = stream()
    column: str = col_name
    target_cols: list[str] = [
        col for col in result_data.columns.tolist() if col.startswith(column)
    ]
    if len(target_cols) == 0:
        raise SpreadSheetFmtErr(f"Expected some cols with the name '{column}'")

    match col_type:
        case "Score":
            target_cols = [
                col
                for col in target_cols
                if col.find(REQ) == -1 and col.find("%") != -1
            ]
        case "Count":
            if col_name != "Attendance":
                raise BadArgumentErr(
                    "Cannot call the function with `col_name` not set to 'Attendance' and `col_type` set to 'Count'."
                )
            target_cols = [
                col
                for col in target_cols
                if col.find(REQ) == -1 and col.find("%") == -1
            ]
        case "Req":
            if col_name == "Project":
                raise BadArgumentErr(
                    "Cannot call the function with `col_name` set to 'Project' and `col_type` set to 'Req'."
                )
            target_cols = [
                col
                for col in target_cols
                if col.find(REQ) != -1 and col.find("%") == -1
            ]

    if len(target_cols) == 0:
        raise SpreadSheetFmtErr(
            f"Expected at least 1 col with name '{col_name}' but without the name '{REQ}'"
        )
    return target_cols[0]


def find_count(col_name: str) -> int | None:
    item: re.Match[str] | None = re.search(r"(\d+)", col_name)
    if item is None:
        return None
    item_str: str = item.group(0)
    return int(item_str)

from pathlib import Path
from typing import cast

import pandas as pd

from pylms.cli import select_student
from pylms.constants import ValidateDataFn
from pylms.errors import LMSError
from pylms.lms.utils import val_result_data
from pylms.utils import DataStore, DataStream, paths, print_stream, read_data


def view_result(ds: DataStore) -> None:
    result_path: Path = paths.get_paths_excel()["Result"]
    if not result_path.exists():
        raise LMSError(
            "Results has not been generated yet. Please collate results before running this operation"
        )

    result_data: pd.DataFrame = read_data(result_path)
    result_stream: DataStream = DataStream(
        result_data, cast(ValidateDataFn, val_result_data)
    )
    serials: list[int] = select_student(ds)
    print_stream(result_stream, serials)

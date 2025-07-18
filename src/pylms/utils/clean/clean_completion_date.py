from datetime import datetime

import pandas as pd

from pylms.constants import COMPLETION, COMPLETION_FMT
from pylms.utils.data import DataStream
from pylms.utils.date import format_date


def _clean_date(entry: str | datetime, day_first: bool) -> str:
    return format_date(entry, COMPLETION_FMT, day_first=day_first)


def clean_completion_date(
    data_stream: DataStream[pd.DataFrame],
) -> DataStream[pd.DataFrame]:
    from pylms.cli import input_option
    data: pd.DataFrame = data_stream()
    format_options: list[str] = ["day first", "month first"]
    _, fmt = input_option(
        format_options,
        title="\nSelect the date format for the NYSC SIWES Completion Month\n",
    )
    day_first = fmt == format_options[0]
    data[COMPLETION] = data[COMPLETION].apply(
        lambda x: _clean_date(x, day_first=day_first)
    )
    return DataStream(data)

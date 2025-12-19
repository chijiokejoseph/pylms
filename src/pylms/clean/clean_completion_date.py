from collections.abc import Callable
from datetime import datetime

import pandas as pd

from ..cli.option_input import input_option
from ..constants import COMPLETION, COMPLETION_FMT
from ..data import DataStream
from ..date import format_date
from ..errors import Result


def _clean_date(entry: str | datetime, day_first: bool) -> str:
    return format_date(entry, COMPLETION_FMT, day_first=day_first)


def clean_completion_date(
    data_stream: DataStream[pd.DataFrame],
) -> Result[DataStream[pd.DataFrame]]:
    data: pd.DataFrame = data_stream()
    format_options: list[str] = ["day first", "month first"]
    result = input_option(
        format_options,
        title="\nSelect the date format for the NYSC SIWES Completion Month\n",
    )
    if result.is_err():
        return result.propagate()

    _, fmt = result.unwrap()
    day_first = fmt == format_options[0]

    def apply() -> Callable[[str], str]:
        return lambda x: _clean_date(x, day_first=day_first)

    data[COMPLETION] = data[COMPLETION].apply(apply())  # pyright: ignore [reportUnknownMemberType]
    return Result.ok(DataStream(data))

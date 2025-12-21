from collections.abc import Callable
from datetime import datetime

import pandas as pd

from ..cli.option_input import input_option
from ..constants import COMPLETION, COMPLETION_FMT
from ..data import DataStream
from ..date import format_date
from ..errors import Result


def _clean_date(entry: str | datetime, day_first: bool) -> str:
    """Format a single completion date entry using the configured format.

    This helper wraps `format_date` with the project's `COMPLETION_FMT`.
    It accepts either a string or a `datetime` and formats it according to the
    provided `day_first` parsing preference.

    Args:
        entry (str | datetime): The date value to format.
        day_first (bool): If True, parsing treats the day as the first field.

    Returns:
        str: The formatted date string according to `COMPLETION_FMT`.
    """
    return format_date(entry, COMPLETION_FMT, day_first=day_first)


def clean_completion_date(
    data_stream: DataStream[pd.DataFrame],
) -> Result[DataStream[pd.DataFrame]]:
    """Normalize the NYSC/SIWES completion month column in a DataStream.

    Prompts the user to choose the input date ordering (\"day first\" or
    \"month first\") and applies a consistent formatting to the column named
    by the `COMPLETION` constant. The formatted DataFrame is returned wrapped
    in a `Result.ok(DataStream(...))`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to transform.

    Returns:
        Result[DataStream[pd.DataFrame]]: Ok result wrapping the transformed
            DataStream, or an error `Result` propagated from the input prompt
            when the user cancels or an invalid selection occurs.
    """
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
        """Return a callable that formats entries using the chosen ordering."""
        return lambda x: _clean_date(x, day_first=day_first)

    data[COMPLETION] = data[COMPLETION].apply(apply())  # pyright: ignore [reportUnknownMemberType]
    return Result.ok(DataStream(data))

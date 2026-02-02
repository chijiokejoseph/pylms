from collections.abc import Callable
from datetime import datetime

import numpy as np
import polars as pl

from pylms.data import datamap

from ..cli.option_input import input_option
from ..constants import COMPLETION, COMPLETION_FMT
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
    data: pl.DataFrame,
) -> Result[pl.DataFrame]:
    """Normalize the NYSC/SIWES completion month column in a pl.DataFrame.

    Prompts the user to choose the input date ordering (\"day first\" or
    \"month first\") and applies a consistent formatting to the column named
    by the `COMPLETION` constant. The formatted DataFrame is returned wrapped
    in a `Result.ok(pl.DataFrame(...))`.

    Args:
        data (pl.DataFrame): The DataFrame to transform.

    Returns:
        Result[pl.DataFrame]: Ok result wrapping a `pl.DataFrame` to indicate success, or an error
        `Result` propagated from the input prompt when the user cancels or an
        invalid selection occurs.
    """
    format_options = ["day first", "month first"]
    result = input_option(
        format_options,
        title="NYSC/SIWES Completion Date",
        prompt="Select the appropriate date format",
    )
    if result.is_err():
        return result.propagate()

    _, fmt = result.unwrap()
    day_first = fmt == format_options[0]

    
    def apply() -> Callable[[str], str]:
        """Return a callable that formats entries using the chosen ordering."""
        return lambda x: _clean_date(x, day_first=day_first)

    # completion: np.ndarray = data[COMPLETION].to_numpy()
    # completion = apply(completion)
    # completion = np.array(completion, dtype=np.str_)
    # data = data.with_columns(pl.Series(COMPLETION, completion, dtype=pl.String))

    apply_func = np.vectorize(apply())

    data = datamap(data, COMPLETION, apply_func, np.str_, pl.String())
    return Result.ok(data)

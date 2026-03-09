import polars as pl

from ..constants import COMPLETION, COMPLETION_FMT
from ..errors import Result


def clean_completion_date(
    data: pl.DataFrame,
) -> Result[pl.DataFrame]:
    """Normalize the NYSC/SIWES completion month column in a pl.DataFrame.

    Applies a consistent formatting to the column named
    by the `COMPLETION` constant. The formatted DataFrame is returned wrapped
    in a `Result.ok(pl.DataFrame(...))`.

    Args:
        data (pl.DataFrame): The DataFrame to transform.

    Returns:
        Result[pl.DataFrame]: Ok result wrapping a `pl.DataFrame` to indicate success, or an error
        `Result` propagated from the input prompt when the user cancels or an
        invalid selection occurs.
    """

    data = data.with_columns(
        pl.col(COMPLETION).str.to_datetime().dt.strftime(COMPLETION_FMT)
    )
    return Result.ok(data)

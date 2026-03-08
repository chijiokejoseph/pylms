import polars as pl

from ..constants import NA


def clean_str(
    data: pl.DataFrame,
    target: str | list[str],
    fill: str = NA,
) -> pl.DataFrame:
    """Ensure specified DataFrame columns contain string values.

    Converts non-string entries in the specified column(s) to strings using
    the `_clean_str` helper. If an element cannot be converted it will be
    replaced with the provided `fill` value. `target_cols` may be either a
    single column name or a list of column names.

    Args:
        data (pl.DataFrame): The
            DataFrame to process.
        target (str | list[str]): Column name or list of column names to
            normalize to strings.
        fill (str): String used to replace elements that cannot be converted.

    Returns:
        None
    """

    target = [target] if isinstance(target, str) else target
    data = data.with_columns(
        [pl.col(col).cast(pl.String).fill_null(fill).alias(col) for col in target]
    )

    return data

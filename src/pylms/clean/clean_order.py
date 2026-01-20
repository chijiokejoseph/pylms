import polars as pl

from pylms.data import DataStream

from ..constants import COMMA_DELIM, DATA_COLUMNS
from ..errors import Result


def clean_order(
    data: pl.DataFrame,
) -> Result[pl.DataFrame]:
    """Validate and reorder DataFrame columns according to the known schema.

    This function attaches a validator that ensures every column in the
    provided DataFrame is one of the expected `DATA_COLUMNS`. After validation
    it selects and returns the DataFrame with columns ordered as in
    `DATA_COLUMNS`, wrapped in a `pl.DataFrame`.

    Args:
        data (pl.DataFrame): The
            DataFrame to validate and reorder.

    Returns:
        pl.DataFrame: pl.DataFrame wrapping the DataFrame whose
            columns are ordered and validated against `DATA_COLUMNS`.
    """

    def validator(test_data: pl.DataFrame) -> tuple[bool, str]:
        missing_cols = [col for col in test_data.columns if col not in DATA_COLUMNS]
        if len(missing_cols):
            cols_print = COMMA_DELIM.join(missing_cols)
            msg = f"The following cols: '{cols_print}' are required but are missing"
            return False, msg
        return True, ""

    result = DataStream.verify(data, validator)
    if result.is_err():
        return result.propagate()

    data = data.select([pl.col(col) for col in DATA_COLUMNS])
    return Result.ok(pl.DataFrame(data))

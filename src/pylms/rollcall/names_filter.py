import polars as pl

from ..constants import COMMA_DELIM, DATE, DATE_FMT, NAME, TIME
from ..data import DataStream
from ..errors import Result
from ..form_utils import defmt_name


def filter_names(turnout_stream: DataStream) -> Result[DataStream]:
    """Filter attendance data to include only entries from the correct date.

    Args:
        turnout_stream (DataStream): Stream containing attendance data.

    Returns:
        DataStream: Filtered stream with only matching date entries.
    """

    def validator(test_data: pl.DataFrame) -> tuple[bool, str]:
        required = {DATE, NAME, TIME}
        columns = set(test_data.columns)

        missing_cols = list(required - columns)
        if len(missing_cols) > 0:
            cols_print = COMMA_DELIM.join(missing_cols)
            msg = f"Missing required columns: {cols_print}"
            return False, msg

        return True, ""

    result = DataStream.verify(turnout_stream.as_ref(), validator)
    if result.is_err():
        return result.propagate()

    turnout_data = turnout_stream.as_ref()

    # Filter data to include only matching dates
    filtered_data = turnout_data.filter(
        pl.col(TIME).str.strptime(pl.Datetime).dt.strftime(DATE_FMT) == pl.col(DATE)
    ).unique(pl.col(NAME))
    filtered_data = defmt_name(DataStream(filtered_data))
    return filtered_data

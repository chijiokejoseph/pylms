import polars as pl

from pylms.errors import Result

from ..constants import COMMA_DELIM, DATE, DATE_FMT, NAME, TIME
from ..data import DataStream
from ..date import format_date


def _get_time_idx(
    form_timestamps: list[str], class_date_in: str, day_first: bool
) -> list[bool]:
    """Get boolean index for timestamps matching class date.

    Args:
        form_timestamps (list[str]): List of timestamp strings.
        class_date_in (str): Target class date to match.
        day_first (bool): Whether day comes first in date format.

    Returns:
        list[bool]: Boolean list indicating matching timestamps.
    """
    # Convert timestamps to date strings
    timestamp_list = [
        format_date(each_timestamp, DATE_FMT, day_first=day_first)
        for each_timestamp in form_timestamps
    ]
    # Check if each timestamp matches the class date
    return [timestamp_as_date == class_date_in for timestamp_as_date in timestamp_list]


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

    # Get date for which attendance is being marked
    class_date: str = turnout_data[0, DATE]
    # Get the timestamps
    timestamps: list[str] = turnout_data[TIME].to_list()

    idx = _get_time_idx(timestamps, class_date, True)
    if not any(idx):
        idx = _get_time_idx(timestamps, class_date, False)

    # Filter data to include only matching dates
    filtered_data = turnout_data.filter(pl.Series(idx))
    return Result.ok(DataStream(filtered_data))

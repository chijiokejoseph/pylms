import pandas as pd

from pylms.constants import DATE, DATE_FMT, NAME, TIME
from pylms.utils import DataStream, date


def filter_names(turnout_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    def validator(test_data: pd.DataFrame) -> bool:
        return (
            DATE in test_data.columns.tolist()
            and NAME in test_data.columns.tolist()
            and TIME in test_data.columns.tolist()
        )

    turnout_stream = DataStream(turnout_stream(), validator)
    # get date for which attendance is being marked
    class_date: str = turnout_stream()[DATE].iloc[0]
    # get the timestamps at which those names are filled
    timestamp: pd.Series = turnout_stream()[TIME]

    def get_time_idx(
        form_timestamps: pd.Series, class_date_in: str, day_first: bool
    ) -> list[bool]:
        # convert the timestamps to a list[str] with each timestamp mapped to "dd-mm-yyyy" strings
        timestamp_list: list[str] = [
            date.format_date(each_timestamp, DATE_FMT, day_first=day_first)
            for each_timestamp in form_timestamps.tolist()
        ]
        # check if each timestamp is the same date as the (date for which the attendance is being marked)
        return [
            timestamp_as_date == class_date_in for timestamp_as_date in timestamp_list
        ]

    idx: list[bool] = get_time_idx(timestamp, class_date, True)
    if not any(idx):
        idx = get_time_idx(timestamp, class_date, False)

    # remove names that were filled on a different date than the attendance's date.
    turnout_data: pd.DataFrame = turnout_stream().loc[idx, :]
    return DataStream(turnout_data)

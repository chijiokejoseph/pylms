import pandas as pd

from ..constants import EMAIL
from ..data import DataStream


def clean_email(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """Normalize email addresses in the DataStream's DataFrame.

    Convert entries in the column named by `EMAIL` to lower case and strip
    surrounding whitespace. The operation is applied to the DataFrame obtained
    from `data_stream` and the resulting DataFrame is returned wrapped in a
    `DataStream`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame with an email column to normalize.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the DataFrame with
            normalized email addresses.
    """
    data: pd.DataFrame = data_stream()

    def apply(x: str) -> str:
        """Return a normalized email string (lowercased and stripped)."""
        return x.lower().strip()

    data[EMAIL] = data[EMAIL].apply(apply)  # pyright: ignore [reportUnknownMemberType]
    return DataStream(data)

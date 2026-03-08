import polars as pl

from ..config import Config
from ..constants import AWARDEES, COHORT
from ..data import DataStore, DataStream, read, write
from ..errors import Result, Unit
from ..paths import get_fast_track_path, get_merged_path, get_merit_path
from ..result_utils import val_awardees


def collate_merge(config: Config, ds: DataStore) -> Result[Unit]:
    """Merge merit and fast-track awardees into single file.

    Combines merit-based and fast-track awardees data, removes duplicates,
    and formats the merged data for final certificate generation.

    Args:
        config (Config): Configuration object with cohort details.
        ds (DataStore): DataStore containing cohort information.

    Returns:
        Result[Unit]: Success or error with message.
    """
    cohort_num = ds.as_ref()[0, COHORT]
    merged_path = get_merged_path(config, cohort_num)
    if merged_path.is_err():
        return merged_path.propagate()
    merged_path = merged_path.unwrap()

    fast_track_path = get_fast_track_path(config, cohort_num)
    if fast_track_path.is_err():
        return fast_track_path.propagate()
    fast_track_path = fast_track_path.unwrap()

    if not fast_track_path.exists():
        msg = "Cannot merge merit results with fast track results as fast track results do not exits."
        return Result.err(msg)

    fasttrack = read(fast_track_path)
    if fasttrack.is_err():
        return fasttrack.propagate()
    fasttrack = fasttrack.unwrap()

    merit_path = get_merit_path(config, cohort_num)
    if merit_path.is_err():
        return merit_path.propagate()
    merit_path = merit_path.unwrap()

    if not merit_path.exists():
        msg = "Cannot merge fast track results with merit results as merit results do not yet exist."
        return Result.err(msg)

    merit = read(merit_path)
    if merit.is_err():
        return merit.propagate()
    merit = merit.unwrap()

    result = DataStream.verify(merit, val_awardees)
    if result.is_err():
        return result.propagate()

    result = DataStream.verify(fasttrack, val_awardees)
    if result.is_err():
        return result.propagate()

    # Merge the data vertically
    merged = pl.concat([merit, fasttrack], how="vertical")

    # Remove rows that are completely null
    merged = merged.filter(~pl.all_horizontal(pl.all().is_null()))

    # Convert to string and replace null values with empty strings
    merged = merged.cast({pl.Utf8: pl.String}).fill_null("")

    # Remove duplicates based on email and phone
    merged = merged.unique(subset=[AWARDEES["Email"], AWARDEES["Phone"]])

    name_col = AWARDEES["Name"]
    email_col = AWARDEES["Email"]
    phone_col = AWARDEES["Phone"]

    # Format names and emails
    merged = merged.with_columns(
        [
            pl.col(name_col).str.strip_chars().str.to_titlecase(),
            pl.col(email_col).str.strip_chars().str.to_lowercase(),
            pl.col(phone_col).cast(pl.Utf8),
        ]
    )

    # Sort by name and reset index
    merged = merged.sort(AWARDEES["Name"])

    result = write(merged, merged_path)
    if result.is_err():
        return result.propagate()

    return Result.unit()

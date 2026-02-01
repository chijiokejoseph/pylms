import polars as pl

from ..constants import AWARDEES, COHORT
from ..data import DataStore, DataStream, read
from ..errors import Result, Unit
from ..paths import get_fast_track_path, get_merged_path, get_merit_path


def _val_awardees(test_data: pl.DataFrame) -> bool:
    """Validate awardees data format.
    
    Args:
        test_data (pl.DataFrame): Awardees data to validate.
        
    Returns:
        bool: True if data contains all required awardees columns.
    """
    required_cols = [
        AWARDEES["Batch"],
        AWARDEES["BatchID"],
        AWARDEES["CertID"],
        AWARDEES["CourseTitle"],
        AWARDEES["Date"],
        AWARDEES["Email"],
        AWARDEES["Name"],
        AWARDEES["Phone"],
    ]
    columns = test_data.columns
    return all(col in columns for col in required_cols)


def collate_merge(ds: DataStore) -> Result[Unit]:
    """Merge merit and fast-track awardees into single file.
    
    Combines merit-based and fast-track awardees data, removes duplicates,
    and formats the merged data for final certificate generation.
    
    Args:
        ds (DataStore): DataStore containing cohort information.
        
    Returns:
        Result[Unit]: Success or error with message.
    """
    cohort_num = ds.as_ref()[0, COHORT]
    merged_path = get_merged_path(cohort_num)
    if merged_path.is_err():
        return merged_path.propagate()
    merged_path = merged_path.unwrap()

    fast_track_path = get_fast_track_path(cohort_num)
    if fast_track_path.is_err():
        return fast_track_path.propagate()
    fast_track_path = fast_track_path.unwrap()

    if not fast_track_path.exists():
        msg = "Cannot merge merit results with fast track results as fast track results do not exits."
        return Result.err(msg)

    fast_track_data = read(fast_track_path)
    if fast_track_data.is_err():
        return fast_track_data.propagate()
    fast_track_data = fast_track_data.unwrap()

    merit_path = get_merit_path(cohort_num)
    if merit_path.is_err():
        return merit_path.propagate()
    merit_path = merit_path.unwrap()

    if not merit_path.exists():
        msg = "Cannot merge fast track results with merit results as merit results do not yet exist."
        return Result.err(msg)

    merit_data = read(merit_path)
    if merit_data.is_err():
        return merit_data.propagate()
    merit_data = merit_data.unwrap()

    merit_data = DataStream(merit_data, _val_awardees).as_ref()
    fast_track_data = DataStream(fast_track_data, _val_awardees).as_ref()

    # Merge the data vertically
    merged_data = pl.concat([merit_data, fast_track_data], how="vertical")
    
    # Remove rows that are completely null
    merged_data = merged_data.filter(~pl.all_horizontal(pl.all().is_null()))
    
    # Convert to string and replace null values with empty strings
    merged_data = merged_data.cast(pl.Utf8).fill_null("")
    
    # Remove duplicates based on email and phone
    merged_data = merged_data.unique(subset=[AWARDEES["Email"], AWARDEES["Phone"]])

    name_col = AWARDEES["Name"]
    email_col = AWARDEES["Email"]
    phone_col = AWARDEES["Phone"]

    # Format names and emails
    merged_data = merged_data.with_columns([
        pl.col(name_col).str.strip_chars().str.to_titlecase(),
        pl.col(email_col).str.strip_chars().str.to_lowercase(),
        pl.col(phone_col).cast(pl.Utf8)
    ])
    
    # Sort by name and reset index
    merged_data = merged_data.sort(AWARDEES["Name"])

    result = DataStream(merged_data).to_excel(merged_path)
    if result.is_err():
        return result.propagate()

    return Result.unit()

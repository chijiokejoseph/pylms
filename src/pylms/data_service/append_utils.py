from ..clean import clean_attendance, clean_duplicates, clean_sort
from ..data import DataStore


def clean_after_ops(ds: DataStore) -> None:
    """Clean DataStore after operations by updating serials and sorting.

    Args:
        ds (DataStore): DataStore to clean and update.
    """
    data_ref = ds.as_ref()
    # Update unique columns, sort by name, and reset serial numbers
    data_ref = clean_duplicates(data_ref)
    data_ref = clean_sort(data_ref)

    # Clean date columns
    data_ref = clean_attendance(data_ref)
    _ = ds.copy_from(data_ref).unwrap()

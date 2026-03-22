from ..data import DataStore, DataStream
from ..errors import Result, Unit
from ..info import print_info
from ..models import UpdateFormInfo
from ..preprocess import clean_new_data
from .add import add


def append_update(
    ds: DataStore, update_stream: DataStream, info: UpdateFormInfo
) -> Result[Unit]:
    """Append update form data to existing DataStore.

    Args:
        ds (DataStore): Target DataStore to update.
        update_stream (DataStream): New data from update form.
        info (UpdateFormInfo): Form information including week number.

    Returns:
        Result[Unit]: Success or error message.
    """
    week_num = info.week_num

    # Clean and validate new data
    new_ds = clean_new_data(update_stream, ds)
    if new_ds.is_err():
        return new_ds.propagate()

    new_ds = new_ds.unwrap()
    new_ds = add(ds, new_ds)

    if new_ds.is_err():
        return new_ds.propagate()

    new_ds = new_ds.unwrap()

    print_info(
        f"Entries retrieved from the Data Form for Week {week_num} have been saved"
    )
    return ds.copy_from(new_ds)

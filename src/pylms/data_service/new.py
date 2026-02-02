from ..clean import normalize
from ..data import DataStore
from ..errors import Result
from ..history import History
from ..info import print_info, printpass
from ..paths import get_paths_excel
from ..preprocess import clean_reg_data
from .load import load_ds
from .save import save_ds


def init_ds(history: History) -> Result[DataStore]:
    """Create new DataStore from registration data with preprocessing.

    Args:
        history (History): History object for tracking operations.

    Returns:
        Result[DataStore]: Success with new DataStore or error message.
    """
    if get_paths_excel()["DataStore"].exists():
        ds = load_ds()
        if ds.is_err():
            return ds.propagate()

        ds = ds.unwrap()
        print_info("DataStore has been loaded")
        return Result.ok(ds)

    # Clean and preprocess registration data
    ds = clean_reg_data()
    if ds.is_err():
        return ds.propagate()
    ds = ds.unwrap()

    result = normalize(ds, history)
    if result.is_err():
        return result.propagate()

    result = save_ds(ds)
    if result.is_err():
        return result.propagate()

    printpass("DataStore has been initialized successfully.")
    return Result.ok(ds)

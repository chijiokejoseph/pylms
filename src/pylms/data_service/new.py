from ..clean import normalize
from ..config import Config
from ..data import DataStore
from ..errors import Result
from ..history import History
from ..info import print_info, printpass
from ..paths import get_paths_excel
from ..preprocess import clean_reg_data
from .load import load_ds
from .save import save_ds


def init_ds(config: Config, history: History) -> Result[DataStore]:
    """Create new DataStore from registration data with preprocessing.

    Args:
        config: Application configuration.
        history: History object for tracking operations.

    Returns:
        Result[DataStore]: Success with new DataStore or error message.
    """
    if get_paths_excel(config)["DataStore"].exists():
        ds = load_ds(config)
        if ds.is_err():
            return ds.propagate()

        ds = ds.unwrap()
        print_info("DataStore has been loaded")
        return Result.ok(ds)

    ds = clean_reg_data()
    if ds.is_err():
        return ds.propagate()
    ds = ds.unwrap()

    result = normalize(ds, history)
    if result.is_err():
        return result.propagate()

    result = save_ds(config, ds)
    if result.is_err():
        return result.propagate()

    printpass("DataStore has been initialized successfully.")
    return Result.ok(ds)

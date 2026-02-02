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
    if get_paths_excel()["DataStore"].exists():
        app_ds = load_ds()
        if app_ds.is_err():
            return app_ds.propagate()

        app_ds = app_ds.unwrap()
        print_info("DataStore has been loaded")
        return Result.ok(app_ds)
    app_ds = clean_reg_data()
    if app_ds.is_err():
        return app_ds.propagate()
    app_ds = app_ds.unwrap()

    result = normalize(app_ds, history)
    if result.is_err():
        return result.propagate()

    app_ds.prefilled = False

    result = save_ds(app_ds)
    if result.is_err():
        return result.propagate()

    printpass("Preprocessing operation completed successfully.")
    return Result.ok(app_ds)

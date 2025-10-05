from pylms.errors import Result
from pylms.utils import DataStore, paths
from pylms.data_ops.load import load
from pylms.preprocess import clean_reg_data, normalize
from pylms.history import History


def new(history: History) -> Result[DataStore]:
    if paths.get_paths_excel()["DataStore"].exists():
        app_ds: DataStore = load()
        print(
            "Preprocessing already performed before. Hence data is not preprocessed again"
        )
        return Result[DataStore].ok(app_ds)

    app_ds_result = clean_reg_data()
    if app_ds_result.is_err():
        return Result[DataStore].err(app_ds_result.unwrap_err())
    app_ds = app_ds_result.unwrap()
    normalize(app_ds, history)
    app_ds.prefilled = False
    print("Preprocessing operation completed successfully.")
    return Result[DataStore].ok(app_ds)

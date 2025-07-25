from pylms.utils import DataStore, paths
from pylms.data_ops.load import load
from pylms.preprocess import clean_reg_data, normalize
from pylms.history import History


def new(history: History) -> DataStore:
    if paths.get_paths_excel()["DataStore"].exists():
        app_ds: DataStore = load()
        print(
            "Preprocessing already performed before. Hence data is not preprocessed again"
        )
        return app_ds

    app_ds = clean_reg_data()
    normalize(app_ds, history)
    app_ds.prefilled = False
    print("Preprocessing operation completed successfully.")
    return app_ds

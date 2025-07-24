from pylms.utils import DataStore, paths
from pylms.data_ops.load_utils import _make_weekly_ds
from pylms.data_ops.load import load
from pylms.preprocess import clean_reg_data


def new() -> DataStore:
    if paths.get_paths_excel()["DataStore"].exists():
        app_ds: DataStore = load()
        print(
            "Preprocessing already performed before. Hence data is not preprocessed again"
        )
    else:
        app_ds = clean_reg_data()
        print("Preprocessing operation completed successfully.")
    _make_weekly_ds(app_ds)
    return app_ds

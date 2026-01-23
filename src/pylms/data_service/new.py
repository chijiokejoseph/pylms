from ..clean import normalize
from ..data import DataStore
from ..errors import Result
from ..history import History
from ..info import print_info, printpass
from ..paths import get_paths_excel
from ..preprocess import clean_reg_data
from .load import load


def new(history: History) -> Result[DataStore]:
    if get_paths_excel()["DataStore"].exists():
        ds = load()
        if ds.is_err():
            return ds.propagate()

        ds = ds.unwrap()
        print_info(
            "Preprocessing already performed before. Hence data is not preprocessed again"
        )
        return Result.ok(ds)

    ds = clean_reg_data()
    if ds.is_err():
        return ds.propagate()
    ds = ds.unwrap()

    result = normalize(ds, history)
    if result.is_err():
        return result.propagate()

    printpass("Preprocessing operation completed successfully.")
    return Result.ok(ds)

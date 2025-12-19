import pandas as pd

from ..constants import DATA_COLUMNS, SPACE_DELIM
from ..data import DataStore
from ..errors import Result, Unit, eprint
from .append_utils import clean_after_ops


def add(superset: DataStore, subset: DataStore) -> Result[DataStore]:
    superset_ref: pd.DataFrame = superset.as_ref()
    subset_ref: pd.DataFrame = subset.as_ref()
    superset_cols: list[str] = superset_ref.columns.tolist()
    subset_cols: list[str] = subset_ref.columns.tolist()

    def validate_subset() -> Result[Unit]:
        superset_extras: list[str] = [
            col for col in superset_cols if col not in DATA_COLUMNS
        ]
        subset_extras: list[str] = [
            col for col in subset_cols if col not in DATA_COLUMNS
        ]
        if any([extra_col not in superset_extras for extra_col in subset_extras]):
            msg = f"The following columns in the subset {[col for col in subset_extras if col not in superset_extras]} are not found in the superset DataStore. \nPlease rerun the program with the correct inputs and try again."
            eprint(msg)
            return Result.err(msg)
        return Result.unit()

    result = validate_subset()

    if result.is_err():
        return result.propagate()

    data_dict: dict[str, list[object]] = {}
    subset_num_rows: int = subset().shape[0]
    for column in superset_cols:
        if column in subset_cols:
            new_entry: list[object] = subset_ref[column].tolist()
        else:
            new_entry = [SPACE_DELIM for _ in range(subset_num_rows)]
        data_dict.update({column: new_entry})

    new_rows: pd.DataFrame = pd.DataFrame(data=data_dict)

    new_data: pd.DataFrame = pd.concat([superset_ref, new_rows])
    new_ds = DataStore.from_data(new_data)

    if new_ds.is_err():
        return new_ds.propagate()

    new_ds = new_ds.unwrap()
    clean_after_ops(new_ds)
    return Result.ok(new_ds)

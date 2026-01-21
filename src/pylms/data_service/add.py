import pandas as pd

from ..constants import COMMA_DELIM, DATA_COLUMNS, SPACE_DELIM
from ..data import DataStore
from ..errors import Result, Unit, eprint
from .append_utils import clean_after_ops


def add(superset: DataStore, subset: DataStore) -> Result[DataStore]:
    superset_ref = superset.as_ref()
    subset_ref = subset.as_ref()
    superset_cols = superset_ref.columns.tolist()
    subset_cols = subset_ref.columns.tolist()

    def validate_subset() -> Result[Unit]:
        superset_extras = [col for col in superset_cols if col not in DATA_COLUMNS]
        subset_extras = [col for col in subset_cols if col not in DATA_COLUMNS]
        mismatched_cols = [col for col in subset_extras if col not in superset_extras]
        if len(mismatched_cols) > 0:
            cols_print = COMMA_DELIM.join(mismatched_cols)
            msg = f"The following columns in the subset {cols_print} are not found in the superset DataStore. \nPlease rerun the program with the correct inputs and try again."
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

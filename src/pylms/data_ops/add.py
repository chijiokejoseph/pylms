import sys
from typing import Any

import pandas as pd

from pylms.constants import DATA_COLUMNS, SPACE_DELIM
from pylms.data_ops.append_utils import _clean_up
from pylms.utils.data import DataStore


def add(superset: DataStore, subset: DataStore) -> DataStore:
    superset_cols: list[str] = superset().columns.tolist()
    subset_cols: list[str] = subset().columns.tolist()

    def validate_subset() -> None:
        superset_extras: list[str] = [
            col for col in superset_cols if col not in DATA_COLUMNS
        ]
        subset_extras: list[str] = [
            col for col in subset_cols if col not in DATA_COLUMNS
        ]
        if any([extra_col not in superset_extras for extra_col in subset_extras]):
            sys.exit(
                f"The following columns in the subset {[col for col in subset_extras if col not in superset_extras]} are not found in the superset DataStore. \nPlease rerun the program with the correct inputs and try again."
            )

    validate_subset()

    data_dict: dict[str, list[Any]] = {}
    subset_num_rows: int = subset().shape[0]
    for column in superset_cols:
        if column in subset_cols:
            new_entry: list[Any] = subset()[column].tolist()
        else:
            new_entry = [SPACE_DELIM for _ in range(subset_num_rows)]
        data_dict.update({column: new_entry})

    new_row: pd.DataFrame = pd.DataFrame(data=data_dict)

    new_data: pd.DataFrame = pd.concat([superset(), new_row])
    new_ds: DataStore = DataStore(new_data[DATA_COLUMNS])
    new_ds.data = new_data
    return _clean_up(new_ds)

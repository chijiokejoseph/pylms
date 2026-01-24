import polars as pl

from ..constants import DATA_COLUMNS, SPACE_DELIM
from ..data import DataStore
from ..errors import Result, Unit, eprint
from .append_utils import clean_after_ops


def add(superset: DataStore, subset: DataStore) -> Result[DataStore]:
    """Add subset DataStore to superset DataStore with column validation.
    
    Args:
        superset (DataStore): Target DataStore to add data to.
        subset (DataStore): Source DataStore to add from.
        
    Returns:
        Result[DataStore]: Success with new combined DataStore or error message.
    """
    superset_ref = superset.as_ref()
    subset_ref = subset.as_ref()
    superset_cols: list[str] = superset_ref.columns
    subset_cols: list[str] = subset_ref.columns

    def validate_subset() -> Result[Unit]:
        """Validate that subset columns exist in superset."""
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

    # Align subset columns with superset, filling missing columns with spaces
    subset_ref = subset_ref.lazy().select(
        [
            pl.when(col in superset_ref.columns)
            .then(pl.col(col))
            .otherwise(
                pl.Series(col, [SPACE_DELIM for _ in range(subset_ref.shape[0])])
            )
            for col in subset_ref.columns
        ]
    ).collect()

    # Combine DataFrames vertically
    new = superset_ref.vstack(subset_ref)
    new = DataStore.from_data(new)

    if new.is_err():
        return new.propagate()

    new = new.unwrap()
    clean_after_ops(new)
    return Result.ok(new)

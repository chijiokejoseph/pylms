import polars as pl

from ..constants import DATA_COLUMNS, SPACE_DELIM
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..history import History
from .append_utils import clean_after_ops


def add(superset: DataStore, subset: DataStore, history: History) -> Result[DataStore]:
    """Add subset DataStore to superset DataStore with column validation.

    Args:
        superset (DataStore): Target DataStore to add data to.
        subset (DataStore): Source DataStore to add from.
        history (History): History object

    Returns:
        Result[DataStore]: Success with new combined DataStore or error message.
    """
    superset_ref = superset.as_ref()
    subset_ref = subset.as_ref()
    superset_cols = superset_ref.columns
    subset_cols = subset_ref.columns

    def validate_subset() -> Result[Unit]:
        """Validate that subset columns exist in superset."""
        superset_extras = [col for col in superset_cols if col not in DATA_COLUMNS]
        subset_extras = [col for col in subset_cols if col not in DATA_COLUMNS]
        if any([extra_col not in superset_extras for extra_col in subset_extras]):
            msg = f"The following columns in the subset {[col for col in subset_extras if col not in superset_extras]} are not found in the superset DataStore. \nPlease rerun the program with the correct inputs and try again."
            eprint(msg)
            return Result.err(msg)
        return Result.unit()

    result = validate_subset()

    if result.is_err():
        return result.propagate()

    # Align subset columns with superset, filling missing columns with spaces
    missing_cols = [
        col for col in superset_ref.columns if col not in subset_ref.columns
    ]
    subset_ref = subset_ref.with_columns(
        [
            pl.Series(col, [SPACE_DELIM for _ in range(subset_ref.height)]).alias(col)
            for col in missing_cols
        ]
    ).select(superset_ref.columns)

    col_types = [superset_ref.get_column(col).dtype for col in superset_ref.columns]
    subset_ref = subset_ref.with_columns(
        [
            pl.col(col).cast(col_type)
            for col_type, col in zip(col_types, superset_ref.columns)
        ]
    )

    # Combine DataFrames vertically
    new = superset_ref.vstack(subset_ref)
    new = DataStore.from_data(new)

    if new.is_err():
        return new.propagate()

    new = new.unwrap()
    clean_after_ops(new, history)
    return Result.ok(new)

import polars as pl

from pylms.constants import COHORT
from pylms.errors import Result, Unit

from ..cli import input_bool, provide_serials
from ..data import DataStore, DataStream
from ..data_service import sub
from ..info import print_info
from .awardees import collate_awardees


def collate_fast_track(ds: DataStore) -> Result[Unit]:
    """Collate fast-track students for advanced class promotion.

    Prompts user to select students for fast-track promotion, confirms selection,
    and generates awardees data while removing them from the main DataStore.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[Unit]: Success or error with message.
    """
    print("Enter the students to be fast tracked to the Advanced Class.")
    student_serials = provide_serials(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()

    choice = input_bool("Confirm the following students should be fast-tracked")
    if choice.is_err():
        return choice.propagate()
    choice = choice.unwrap()

    if not choice:
        print_info("\nFast Tracking has been cancelled.\n")
        return Result.unit()

    student_indices = [serial - 1 for serial in student_serials]
    pretty = ds.pretty()
    fast_track_data = pretty.slice(0).filter(
        pl.int_range(pl.len()).is_in(student_indices)
    )
    cohort: int = pretty[0, COHORT]

    choice = collate_awardees(
        DataStream(fast_track_data), cohort, collate_type="fast track"
    )
    if choice.is_err():
        return choice.propagate()

    print_info(
        "Students fast tracked to the Advanced Class have been collected. Removing them from DataStore."
    )
    return sub(ds, student_serials)

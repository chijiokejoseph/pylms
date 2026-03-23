import polars as pl

from ..cli import input_bool
from ..config import Config
from ..constants import COHORT, EMAIL, NAME, SERIAL
from ..data import DataStore, DataStream
from ..data_service import sub
from ..errors import Result, Unit
from ..history import History
from ..info import print_info
from ..query_data import run_query_data
from .awardees import collate_awardees


def collate_fast_track(config: Config, ds: DataStore, history: History) -> Result[Unit]:
    """Collate fast-track students for advanced class promotion.

    Prompts user to select students for fast-track promotion, confirms selection,
    and generates awardees data while removing them from the main DataStore.

    Args:
        config (Config): Configuration object.
        ds (DataStore): DataStore containing student data.
        history (History): History object

    Returns:
        Result[Unit]: Success or error with message.
    """
    print("Enter the students to be fast tracked to the Advanced Class.")
    student_serials = run_query_data(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()
    pretty = ds.pretty()
    fast_track_data = pretty.filter(pl.col(SERIAL).is_in(student_serials))

    display_data = fast_track_data.select([SERIAL, NAME, EMAIL])
    print_info("Selected students are shown below")
    print(display_data)

    choice = input_bool("Confirm the following students should be fast-tracked")
    if choice.is_err():
        return choice.propagate()
    choice = choice.unwrap()

    if not choice:
        print_info("Fast Tracking has been cancelled.\n")
        return Result.unit()

    cohort: int = pretty[0, COHORT]

    choice = collate_awardees(
        config, history, DataStream(fast_track_data), cohort, collate_type="fast track"
    )
    if choice.is_err():
        return choice.propagate()

    print_info(
        "Students fast tracked to the Advanced Class have been collected. Removing them from DataStore."
    )
    return sub(ds, student_serials)

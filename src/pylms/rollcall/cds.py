import polars as pl

from ..constants import CDS, NAME, WEEK_DAYS
from ..data import DataStore, DataStream
from ..date import to_day_num
from ..errors import Result, Unit
from ..form_utils import defmt_name
from ..record import RecordStatus


def record_cds(ds: DataStore, cds_data_stream: DataStream) -> Result[Unit]:
    """Record CDS (Community Development Service) days for NYSC students.

    Args:
        ds (DataStore): DataStore to update with CDS records.
        cds_data_stream (DataStream): Stream containing CDS day information.
    """
    data_ref = ds.as_ref()
    pretty = ds.pretty()
    cds_data = cds_data_stream.as_ref()
    cds_data = defmt_name(DataStream(cds_data))
    if cds_data.is_err():
        return cds_data.propagate()
    
    cds_data = cds_data.unwrap().as_ref()

    cds_num_col = f"{CDS} Num"
    cds_data = cds_data.with_columns(pl.lit(0).alias(cds_num_col)).with_columns(
        [
            pl.when(pl.col(CDS) == day)
            .then(pl.lit(i))
            .otherwise(pl.col(cds_num_col))
            .alias(cds_num_col)
            for i, day in enumerate(WEEK_DAYS, start=1)
        ]
    )
    sub_data = cds_data.select([NAME, cds_num_col])
    pretty = (
        pretty.join(sub_data, NAME, how="left")
        .with_columns(pl.col(cds_num_col).fill_null(0).alias(cds_num_col))
        .sort(pl.col(NAME))
    )
    date_cols = [col for col in data_ref.columns if col.count("/") == 2]
    pretty = pretty.with_columns(
        [
            # weekday num of date is equal to cds_day_num
            pl.when(to_day_num(date) == pl.col(cds_num_col))
            .then(
                # if existing record is not NO_CLASS
                pl.when(pl.col(date) != str(RecordStatus.NO_CLASS))
                # set CDS
                .then(pl.lit(str(RecordStatus.CDS)))
                .otherwise(pl.col(date))
            )
            .otherwise(pl.col(date))
            .alias(date)
            for date in date_cols
        ]
    )
    data_ref = pretty.drop(cds_num_col).with_columns(
        pl.Series(NAME, data_ref.get_column(NAME)).alias(NAME)
    )
    # ds.copy_from(data_ref)

    # # Get student names and CDS information
    # cds_names: list[str] = cds_data[NAME].to_list()
    # cds_names = [name.title() for name in cds_names]
    # cds_days: list[str] = cds_data[CDS].to_list()

    # # Process each student in the DataStore
    # for i in range(data_ref.height):
    #     student_name = data_ref[i, NAME]

    #     if student_name not in cds_names:
    #         continue

    #     cds_name_idx = cds_names.index(student_name)
    #     cds_day = cds_days[cds_name_idx]

    #     if cds_day not in WORK_DAYS:
    #         continue

    #     cds_day_num = to_day_num(cds_day)

    #     # Update attendance records for matching CDS days
    #     for col in data_ref.columns:
    #         if not col.count("/") == 2:  # Check if column is a date
    #             continue

    #         date_day_num = to_day_num(col)
    #         current_status = data_ref[i, col]

    #         if cds_day_num == date_day_num and current_status != str(
    #             RecordStatus.NO_CLASS
    #         ):
    #             # Update the specific cell
    #             data_ref = data_ref.with_columns(
    #                 pl.when(pl.int_range(pl.len()) == i)
    #                 .then(pl.lit(str(RecordStatus.CDS)))
    #                 .otherwise(pl.col(col))
    #                 .alias(col)
    #             )

    # Update the DataStore with modified data
    return ds.copy_from(data_ref)

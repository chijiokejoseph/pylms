import polars as pl

from ..constants import EMAIL, NAME, SERIAL, SPACE_DELIM
from ..data import DataStore, DataStream
from ..errors import Result, eprint
from ..numutil import det_num_width


def fmt_name(ds: DataStore) -> list[str]:
    pretty = ds.pretty()
    data = pretty.select([NAME, EMAIL, SERIAL])
    max_serial = data.height
    max_serial_len = det_num_width(max_serial)
    data = data.with_columns(
        pl.col(SERIAL).cast(pl.String).str.pad_start(max_serial_len, "0").alias(SERIAL)
    )
    data = data.with_columns(
        pl.concat_str(
            [
                pl.col(SERIAL).cast(pl.String),
                pl.lit(f".{SPACE_DELIM * 2}"),
                pl.col(NAME),
            ],
            separator="",
        ).alias("Result")
    )
    return data["Result"].to_list()


def defmt_name(stream: DataStream) -> Result[DataStream]:
    data = stream.as_ref()
    if NAME not in data.columns:
        msg = f"Expected Column '{NAME}' in data columns. Column not found"
        eprint(msg)
        return Result.err(msg)

    data = data.with_columns(
        pl.col(NAME).str.replace_all(r"\d{3}.\s*", "").str.strip_chars().alias(NAME)
    )
    return Result.ok(DataStream(data))

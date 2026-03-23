import polars as pl


def print_data(data: pl.DataFrame) -> None:
    with pl.Config(tbl_formatting="UTF8_FULL", set_tbl_rows=-1):
        print(data)

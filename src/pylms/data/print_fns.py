from collections.abc import Iterable
from typing import Any

import pandas as pd

from .datastream import DataStream


def _max_print(items: Iterable[Any]) -> int:
    return max([len(str(item)) for item in items])


def print_df(data: pd.DataFrame, serials: list[int]) -> None:
    indices = [i - 1 for i in serials]
    subset = data.loc[indices, :]
    dataset = subset.to_dict(orient="records")  # pyright: ignore[reportUnknownMemberType]
    for entry in dataset:
        max_key = _max_print(entry.keys())
        max_value = _max_print(entry.values())
        for key, value in entry.items():
            print(f"{key:<{max_key}} : {value:<{max_value}}")
        print("\n")


def print_stream(stream: DataStream[pd.DataFrame], serials: list[int]) -> None:
    print_df(stream(), serials)

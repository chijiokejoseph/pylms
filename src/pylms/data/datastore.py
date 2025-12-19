from pathlib import Path
from typing import Callable, Literal, Self, final, override

import pandas as pd

from ..constants import (
    COMMA,
    DATA_COLUMNS,
    NAME,
    PHONE,
    SEMI,
)
from ..errors import LMSError, Result, eprint
from .data_read import read
from .datastream import DataStream

type Validator = Callable[[pd.DataFrame], bool]


def validate(test_data: pd.DataFrame) -> bool:
    data_columns: list[str] = test_data.columns.tolist()
    # compare lengths of expected and actual columns
    if len(data_columns) > len(DATA_COLUMNS):
        eprint(
            f"data argument has more columns than the expected number of columns required for the first initialization of the DataStore. These required columns are {DATA_COLUMNS}. \nCheck it is possible that you are trying to reinitialize a DataStore that has already been initialized."
        )
        return False
    elif len(data_columns) < len(DATA_COLUMNS):
        return False
    else:
        pass
    # comparing that the order and names of expected columns match those of the actual columns.
    for expected, actual in zip(DATA_COLUMNS, data_columns):
        if expected != actual:
            return False
    return True


@final
class DataStore(DataStream[pd.DataFrame]):
    """
    An extension of the DataStream Class. It limits its Generic type from the `pd.DataFrame | pd.Series` to `pd.DataFrame`
    """

    @classmethod
    def from_local(cls, path: Path) -> Result[Self]:
        data = read(path, keep_na=True)
        if data.is_err():
            return data.propagate()
        data = data.unwrap()
        return cls.from_data(data)

    @classmethod
    def from_data(cls, data: pd.DataFrame) -> Result[Self]:
        try:
            subset_data: pd.DataFrame = data[DATA_COLUMNS]
        except KeyError as e:
            msg = f"Failed at from_local, failed to validate the passed in as argument to `data`, because it lacked required columns stored in the constant `DATA_COLUMNS.\nError encountered: {e}`"
            eprint(msg)
            return Result.err(e)

        if not validate(subset_data):
            msg = "Failed at from_local, failed to validate data stored at the file path specified as argument to `path`"
            eprint(msg)
            return Result.err(LMSError(msg))

        ds: Self = cls(subset_data)
        ds.data = data
        return Result.ok(ds)

    def __init__(
        self, data: pd.DataFrame | DataStream[pd.DataFrame], prefilled: bool = False
    ) -> None:
        """

        :param data: (pd.DataFrame | DataStream[pd.DataFrame]) - The data source to be converted to a DataStore
        :type data: pd.DataFrame | DataStream[pd.DataFrame]
        :param prefilled: (bool) - Indicates if the DataStore contains dummy data or not. Defaults to False
        :type prefilled: bool

        :return: returns None
        :rtype: None
        """
        true_data: pd.DataFrame = (
            data().copy() if isinstance(data, DataStream) else data
        )
        self.prefilled: bool = prefilled
        super().__init__(true_data, validate)

    def copy_from(self, ds: Self) -> None:
        self.data = ds.data
        self.prefilled = ds.prefilled

    def pretty(self) -> pd.DataFrame:
        data: pd.DataFrame = self.as_clone()

        def apply_fn(delim: str) -> Callable[[str], str]:
            return lambda x: x.replace(delim, "")

        data[NAME] = data[NAME].astype(str).apply(apply_fn(COMMA))  # pyright: ignore [reportUnknownMemberType]
        data[PHONE] = data[PHONE].astype(str).apply(apply_fn(SEMI))  # pyright: ignore [reportUnknownMemberType]
        return data

    @override
    def to_excel(
        self, path: Path, style: Literal["pretty", "normal"] = "normal"
    ) -> None:
        """
        saves the underlying data of the DataStore instance to a location specified by the `path` argument.
        path is of type `Path`, which is a class obtained from the `pathlib` library defined as `pathlib.Path`.

        specify `style = "pretty"` to remove the formatting markers placed on the `NAME` and `PHONE` columns. else set `style = "normal"` to save the file exactly as it is. Defaults to `"normal"`.

        :param path: (Path): where to save the Excel file.
        :type path: Path
        :param style: (Literal["pretty", "normal"], optional): This defines if the DataStore should remove its formatting markers placed on the underlying data to aid smoother data retrieval and inferencing before saving to an Excel file.
        :type style: Literal["pretty", "normal"]

        :returns: None
        """
        if style == "pretty":
            data: pd.DataFrame = self.pretty()
        else:
            data = self.as_ref()

        data.to_excel(str(path), index=False)  # pyright: ignore [reportUnknownMemberType]

    @property
    def data(self) -> pd.DataFrame:
        return self.as_clone()

    @data.setter
    def data(self, data: pd.DataFrame) -> None:
        def validator(test_data: pd.DataFrame) -> bool:
            input_cols: list[str] = test_data.columns.tolist()
            expected_cols: list[str] = DATA_COLUMNS
            if len(input_cols) < len(expected_cols):
                return False

            input_subset: list[str] = input_cols[: len(expected_cols)]
            for expected, actual in zip(expected_cols, input_subset):
                if expected != actual:
                    return False
            return True

        _ = DataStream(data, validator)
        self._value = (data,)

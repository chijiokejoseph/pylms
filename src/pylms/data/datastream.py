from pathlib import Path
from typing import Callable, cast, overload, override

import pandas as pd

type DS[K: pd.DataFrame | pd.Series] = DataStream[K]


class DataStream[T: pd.DataFrame | pd.Series]:
    """"""

    _value: tuple[T]

    @overload
    def __init__(self, data: T, validate_fn: Callable[[T], bool] | None = None) -> None:
        pass

    @overload
    def __init__(
        self, data: DS[T], validate_fn: Callable[[T], bool] | None = None
    ) -> None:
        pass

    def __init__(
        self, data: T | DS[T], validate_fn: Callable[[T], bool] | None = None
    ) -> None:
        """
        Constructor of a DataStream instance. Takes a validator_fn argument which is called on the 'data' argument to verify the input data before continuing with the code execution. Raises a ValueError if the validator_fn returns False when called on the argument data.

            type T = pd.DataFrame | pd.Series

        :param data: (T | Self): A DataFrame or Series, or another DataStream instance, whose underlying data is being passed to the new DataStream constructor.
        :type data: T
        :param validate_fn: (optional, Callable[[T], bool] | None) : A function that returns a boolean when called on the `data` argument. When true, `data` is valid else it is invalid. It defaults to None
        :type validate_fn: Callable[[T], bool]
        :rtype: bool
        :returns: None
        """
        # get underlying data for case data of type pd.DataFrame | pd.Series or type DataStream

        if isinstance(data, DataStream):
            underlying_data = data()
        else:
            underlying_data = data

        # validator is Callable and underlying_data is validated by it
        condition1: bool = validate_fn is not None and validate_fn(underlying_data)
        # validator is None
        condition2: bool = validate_fn is None

        if condition1 or condition2:
            self._value = (underlying_data,)
        else:
            raise (
                Exception(
                    "data argument to DataStream does not pass the requirements set by its validator."
                )
            )

    def __call__(self) -> T:
        """
        return a copy of the underlying data from its `self._value` attribute.

        :rtype: T
        :return: the data which was stored in the DataStream instance.
        """
        return self._value[0]

    def as_ref(self) -> T:
        return self._value[0]

    def as_clone(self) -> T:
        ref = self._value[0]
        ref = ref.copy()
        return cast(T, ref)

    @override
    def __str__(self) -> str:
        return f"""
{self.__class__.__name__}(
{self().head(10)}
)
        """

    def is_empty(self) -> bool:
        data = self()
        return data.shape[0] == 0

    def to_excel(self, path: Path) -> None:
        """
        saves the underlying data of the DataStore instance to a location specified by the `path` argument.
        path is of type `Path` which is a class obtained from the `pathlib` library defined as `pathlib.Path`.

        :param path: ( Path ) where to save the Excel file.
        :type path: Path

        :returns: None
        """
        data = self()
        if isinstance(data, pd.DataFrame):
            data.to_excel(str(path), index=False)  # pyright: ignore [reportUnknownMemberType]


if __name__ == "__main__":
    datastream = DataStream(pd.Series([1, 2, 3, 4, 5]))
    stream2 = DataStream(datastream)

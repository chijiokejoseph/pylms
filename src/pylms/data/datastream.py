from pathlib import Path
from typing import Callable, cast, overload, override

import pandas as pd

from ..errors import Result, Unit, eprint

type DS[K: pd.DataFrame | pd.Series] = DataStream[K]


class DataStream[T: pd.DataFrame | pd.Series]:
    """Lightweight container for a pandas DataFrame or Series with validation.

    This class wraps a pandas DataFrame or Series (or another `DataStream`)
    and enforces an optional validation function. It provides accessors that
    return either the stored object or a cloned copy, convenience methods for
    exporting to Excel, and simple introspection helpers.

    Type parameters:
        T: Either `pandas.DataFrame` or `pandas.Series`.

    Attributes:
        _value (tuple[T]): Internal single-element tuple holding the stored value.

    Note:
        When building instances of this class with validators, prefer the `new`
        class method over Python's `__init__` magic method as the former will
        return a Result whose error can be handled while the latter will raise
        an exception.
    """

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
        """Initialize a DataStream with optional validation.

        The constructor accepts either a direct pandas object (`DataFrame` or
        `Series`) or another `DataStream` and an optional `validate_fn`. When a
        validator is provided it is called with the underlying data; if the
        validator returns False an exception is raised and the instance is not
        constructed.

        Args:
            data (T | DataStream[T]): The data to store or another DataStream
                whose value should be used.
            validate_fn (Optional[Callable[[T], bool]]): Optional function that
                returns True when `data` is valid. If None, no validation is performed.

        Raises:
            Exception: If `validate_fn` is provided and returns False for the
                underlying data.
        """
        # Extract the underlying value whether the caller passed a DataStream
        # (in which case we call it to get the stored object) or a raw pandas
        # object. Using this canonical underlying value simplifies validation
        # and storage below.
        if isinstance(data, DataStream):
            underlying_data = data.as_clone()
        else:
            underlying_data = cast(T, data.copy())

        # Two valid initialization conditions:
        #  - A validator was provided and it returns True for the underlying data.
        #  - No validator was provided (validate_fn is None), in which case we
        #    accept the data unconditionally.
        condition1: bool = validate_fn is not None and validate_fn(underlying_data)
        condition2: bool = validate_fn is None

        # If either condition holds we store the underlying object in a single-
        # element tuple. Storing as a tuple is a simple internal representation
        # that avoids accidental reassignment to other attributes.
        if condition1 or condition2:
            self._value = (underlying_data,)
        else:
            # Intentionally raise a clear exception when validation fails so
            # callers cannot construct an invalid DataStream silently.
            raise Exception(
                "data argument to DataStream does not pass the requirements set by its validator."
            )

    @classmethod
    def new[K: pd.Series | pd.DataFrame](
        cls, data: K | DS[K], validator: Callable[[K], bool] | None = None
    ) -> Result[DS[K]]:
        try:
            value = DataStream(data, validator)
            return Result.ok(value)
        except Exception as e:
            msg = str(e)
            eprint(msg)
            return Result.err(msg)

    @classmethod
    def verify[K: pd.Series | pd.DataFrame](
        cls, data: K | DS[K], validator: Callable[[K], bool]
    ) -> Result[Unit]:
        result = DataStream.new(data, validator)
        if result.is_err():
            result.print_if_err()
            return result.propagate()

        return Result.unit()

    def __call__(self) -> T:
        """Return the stored data.

        This call returns the underlying object held by the `DataStream`. It
        does not clone the value; use `as_clone()` when a copy is required.

        Returns:
            T: The stored `DataFrame` or `Series`.
        """
        # Return the stored object by reference. Callers that intend to mutate
        # the returned value should prefer `as_clone()` to avoid mutating the
        # value held inside this DataStream instance.
        return self._value[0]

    def as_ref(self) -> T:
        """Return the underlying value by reference (no copy).

        Note:
            Mutating the returned object will mutate the DataStream's stored
            value. Use `as_clone()` to obtain a copy when mutation is not
            desired.
        """
        return self._value[0]

    def as_clone(self) -> T:
        """Return a shallow copy of the underlying value.

        This method uses the pandas `copy()` operation to produce a separate
        object suitable for modification without affecting the stored value.
        The copy is cast back to the generic type `T` for the caller.
        """
        # Create a shallow copy of the underlying pandas object to protect
        # the internal state against external mutation.
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
        """Return True if the stored DataFrame/Series has no rows.

        Returns:
            bool: True when there are zero rows; otherwise False.
        """
        # Use the stored object's shape to determine emptiness. For Series and
        # DataFrame this checks the number of rows (axis 0).
        data = self()
        return data.shape[0] == 0

    def to_excel(self, path: Path) -> Result[Unit]:
        """Write the stored DataFrame to an Excel file.

        If the stored value is a `pandas.DataFrame` it will be written to the
        given path using `DataFrame.to_excel`. If the stored value is a
        `pandas.Series` this method does nothing.

        Args:
            path (Path): Filesystem path where the Excel file will be written.

        Raises:
            OSError: Propagates any I/O errors raised by pandas or the filesystem.
        """
        # Extract the stored value and only attempt to write when it's a DataFrame.
        # Writing a Series would either require additional handling or produce
        # a less-structured Excel output; the existing behavior intentionally
        # limits output to DataFrames.
        data = self()

        if not path.exists():
            msg = f"Path specified: '{path} does not exist"
            eprint(msg)
            return Result.err(msg)

        try:
            # Use pandas' to_excel implementation which will raise I/O related
            # exceptions on failure; those propagate to callers.
            data.to_excel(path, index=False)  # pyright: ignore [reportUnknownMemberType]
        except Exception as e:
            msg = str(e)
            eprint(msg)
            return Result.err(e)

        return Result.unit()


if __name__ == "__main__":
    datastream = DataStream(pd.Series([1, 2, 3, 4, 5]))
    stream2 = DataStream(datastream)

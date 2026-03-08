from collections.abc import Callable
from pathlib import Path
from typing import Self

import polars as pl

from ..errors import Result, Unit
from .utils import write

type Stream = DataStream


class DataStream:
    """Wrapper for Polars DataFrame with validation and I/O operations."""

    _value: tuple[pl.DataFrame]

    def __init__(self, data: pl.DataFrame | Stream) -> None:
        """Initialize DataStream with DataFrame or another DataStream.

        Args:
            data (pl.DataFrame | Stream): Source data.
        """
        # Extract DataFrame reference if input is DataStream
        data = data.as_ref() if isinstance(data, DataStream) else data
        self._value = (data,)

    @classmethod
    def new(
        cls,
        data: pl.DataFrame | Stream,
        validator: Callable[[pl.DataFrame], tuple[bool, str]] | None = None,
    ) -> Result[Self]:
        """Create new DataStream with optional validation.

        Args:
            data (pl.DataFrame | Stream): Source data.
            validator (Callable | None): Optional validation function.

        Returns:
            Result[Self]: Success with DataStream or error message.
        """
        # Clone data to avoid mutations
        value = data.as_clone() if isinstance(data, DataStream) else data.clone()

        if validator is None:
            return Result.ok(cls(value))
        test, msg = validator(value)
        if test:
            return Result.ok(cls(value))

        return Result.err(msg)

    def as_ref(self) -> pl.DataFrame:
        """Get reference to underlying DataFrame.

        Returns:
            pl.DataFrame: Reference to stored DataFrame.
        """
        return self._value[0]

    def as_clone(self) -> pl.DataFrame:
        """Get clone of underlying DataFrame.

        Returns:
            pl.DataFrame: Clone of stored DataFrame.
        """
        return self.as_ref().clone()

    def is_empty(self) -> bool:
        return self.as_ref().shape[0] > 0

    def write(self, path: Path, *, worksheet: str | None = None) -> Result[Unit]:
        """Write DataFrame to file.

        Args:
            path (Path): Output file path.
            worksheet (str | None): Excel worksheet name.

        Returns:
            Result[Unit]: Success or error message.
        """
        data = self.as_ref()
        return write(data, path, worksheet=worksheet)

    @classmethod
    def verify(
        cls, data: pl.DataFrame, validator: Callable[[pl.DataFrame], tuple[bool, str]]
    ) -> Result[Unit]:
        """Verify DataFrame against validator without creating instance.

        Args:
            data (pl.DataFrame): DataFrame to validate.
            validator (Callable): Validation function.

        Returns:
            Result[Unit]: Success or error message.
        """
        result = DataStream.new(data, validator)
        result.print_if_err()
        if result.is_err():
            return result.propagate()

        return Result.unit()

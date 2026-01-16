from collections.abc import Callable
from pathlib import Path
from typing import Self

import polars as pl

from pylms.errors import Result, Unit, eprint

type Stream_ = Stream


class Stream:
    _value: tuple[pl.DataFrame]

    def __init__(self, data: pl.DataFrame | Stream_) -> None:
        data = data.as_ref() if isinstance(data, Stream) else data
        self._value = (data,)

    @classmethod
    def new(
        cls,
        data: pl.DataFrame | Stream_,
        validator: Callable[[pl.DataFrame], tuple[bool, str]] | None = None,
    ) -> Result[Self]:
        value = data.as_clone() if isinstance(data, Stream) else data.clone()

        if validator is None:
            return Result.ok(cls(value))
        test, msg = validator(value)
        if test:
            return Result.ok(cls(value))

        return Result.err(msg)

    def as_ref(self) -> pl.DataFrame:
        return self._value[0]

    def as_clone(self) -> pl.DataFrame:
        return self.as_ref().clone()

    def write(
        self, path: Path, *, worksheet: str | None = None, pretty: bool | None = None
    ) -> Result[Unit]:
        parent = path.parent
        if not parent.exists():
            msg = f"Parent path specified: '{parent} does not exist"
            eprint(msg)
            return Result.err(msg)

        data = self.as_ref()
        _ = pretty

        try:
            match path.suffix:
                case ".csv":
                    data.write_csv(path, include_header=True)
                case ".xlsx":
                    _ = data.write_excel(path, worksheet)
                case ".parquet":
                    data.write_parquet(path)
                case _:
                    msg = f"File output formats are '.csv', '.xlsx' and '.parquet'. Format: '{path.suffix}' not supported"
                    eprint(msg)
                    return Result.err(msg)

        except Exception as e:
            msg = str(e)
            eprint(msg)
            return Result.err(e)

        return Result.unit()


class Records(Stream):
    def __init__(self, value: pl.DataFrame | Stream) -> None:
        self.prefilled: bool = True
        super().__init__(value)

    @classmethod
    def init(
        cls,
        data: pl.DataFrame | Stream_,
        validator: Callable[[pl.DataFrame], tuple[bool, str]] | None = None,
    ) -> Result[Self]:
        value = data.as_clone() if isinstance(data, Stream) else data.clone()

        if validator is None:
            return Result.ok(cls(value))
        test, msg = validator(value)
        if test:
            return Result.ok(cls(value))

        return Result.err(msg)

import sys
from typing import Callable, Self, cast, final


def eprint(msg: str) -> None:
    _ = sys.stderr.write(msg)


class LMSError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


@final
class Unit:
    def __init__(self) -> None:
        self._value = ()


class Result[T]:
    def __init__(self, value: T | None, error: Exception | None) -> None:
        self._value: T | None = value
        self._error: Exception | None = error
        self._preprocess()

    def _preprocess(self) -> None:
        if self._value is None and self._error is None:
            self._error = ValueError("value is None")
        if self._error is not None and self._value is not None:
            self._value = None

    @classmethod
    def ok(cls, value: T) -> Self:
        return cls(value, None)

    @classmethod
    def err(cls, error: Exception) -> Self:
        return cls(None, error)

    @classmethod
    def unit(cls) -> Self:
        return cls.ok(cast(T, Unit()))

    def is_ok(self) -> bool:
        return self._error is None and self._value is not None

    def is_err(self) -> bool:
        return self._error is not None or self._value is None

    def unwrap(self) -> T:
        if self.is_ok():
            assert self._value is not None, "value is None"
            return self._value
        raise ValueError("Result is an error")

    def unwrap_err(self) -> Exception:
        if self.is_err():
            assert self._error is not None, "error is None"
            return self._error
        raise ValueError("Result is not an error")

    def unwrap_or(self, default: T) -> T:
        if self.is_ok():
            assert self._value is not None, "value is None"
            return self._value
        return default

    def unwrap_or_err(self, default: Exception) -> Exception:
        if self.is_err():
            assert self._error is not None, "error is None"
            return self._error
        return default

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        if self.is_ok():
            assert self._value is not None, "value is None"
            return self._value
        return func()

    @property
    def value(self) -> T | None:
        return self._value

    @property
    def error(self) -> Exception | None:
        return self._error


class ResultMap[T]:
    def __init__(self, result: Result[T]) -> None:
        self.result: Result[T] = result

    def map[K](self, func: Callable[[T], K]) -> Result[K]:
        item: Result[T] = self.result
        if item.is_ok():
            assert item.value is not None, "value is None"
            return Result.ok(func(item.value))
        assert item.error is not None, "error is None"
        return Result.err(item.error)

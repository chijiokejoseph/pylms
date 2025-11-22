import sys
from typing import Callable, final


def eprint(msg: str) -> None:
    msg = f"\n⚠️ Error {msg}\n"
    _ = sys.stderr.write(msg)


class LMSError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


class ForcedExitError(LMSError):
    """
    Exception raised for forced exit errors in CLI inputs.

    :param message: (str) - The error message describing the forced exit.
    :type message: str

    :return: (None) - returns None.
    :rtype: None
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


type UnitResult = Result[Unit]
type MapResult[K] = Result[K]


@final
class Unit:
    def __init__(self) -> None:
        self._value = ()


class Result[T]:
    def __init__(self, value: T | None, error: Exception | None) -> None:
        # if value is not None and error is None, I have a good result
        # if value is None or error is not None, I have a bad result
        self._value: T | None = value
        self._error: Exception | None = error
        self._preprocess()

    def _preprocess(self) -> None:
        if self._value is None and self._error is None:
            self._error = ValueError("value is None")
        if self._error is not None and self._value is not None:
            self._value = None

    def propagate[K](self) -> MapResult[K]:
        error = self._error
        return Result(None, error)

    def map[K](self, func: Callable[[T], K]) -> MapResult[K]:
        if self.is_err():
            return self.propagate()
        value = self.unwrap()
        value = func(value)
        return Result(value, None)

    @classmethod
    def ok[K](cls, value: K) -> MapResult[K]:
        return Result(value, None)

    @classmethod
    def err[K](cls, error: Exception) -> MapResult[K]:
        return Result(None, error)

    @classmethod
    def unit(cls) -> UnitResult:
        return Result.ok(Unit())

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

    def print_if_err(self) -> None:
        if not self.is_err():
            return
        err = self.unwrap_err()
        if isinstance(err, LMSError):
            eprint(err.message)
        else:
            eprint(err)

    @property
    def value(self) -> T | None:
        return self._value

    @property
    def error(self) -> Exception | None:
        return self._error

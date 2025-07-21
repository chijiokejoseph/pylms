from typing import Callable

from pylms.errors import LMSError


class InvalidChoiceError(LMSError):
    def __init__(self, message: str, min_selection: int, max_selection: int) -> None:
        super(InvalidChoiceError, self).__init__(message)
        self.min_selection: int = min_selection
        self.max_selection: int = max_selection


class InvalidInputError(LMSError):
    def __init__(self, message: str, validation_fn: Callable, parsing_to: str) -> None:
        super(InvalidInputError, self).__init__(message)
        self.validation_fn: Callable = validation_fn
        self.parsing_to: str = parsing_to


class InvalidSelectionInputError(LMSError):
    def __init__(self, message: str) -> None:
        super(InvalidSelectionInputError, self).__init__(message)


class InvalidPathError(LMSError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ForcedExitError(LMSError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

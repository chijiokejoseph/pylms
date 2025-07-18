from typing import Callable

from pylms.errors import LMSError


class InvalidChoiceError(LMSError):
    def __init__(self, message: str, min_selection: int, max_selection: int) -> None:
        self.message: str = message
        self.min_selection: int = min_selection
        self.max_selection: int = max_selection
        super(InvalidChoiceError, self).__init__(message)


class InvalidInputError(LMSError):
    def __init__(self, message: str, validation_fn: Callable, parsing_to: str) -> None:
        self.message: str = message
        self.validation_fn: Callable = validation_fn
        self.parsing_to: str = parsing_to
        super(InvalidInputError, self).__init__(message)


class InvalidSelectionInputError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super(InvalidSelectionInputError, self).__init__(message)


class InvalidPathError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super(InvalidPathError, self).__init__(message)


class ForcedExitError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)

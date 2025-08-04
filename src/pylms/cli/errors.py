from typing import Callable

from pylms.errors import LMSError


class InvalidChoiceError(LMSError):
    """
    Exception raised for invalid choice errors in CLI inputs.

    :param message: (str) - The error message describing the invalid choice.
    :type message: str
    :param min_selection: (int) - The minimum valid selection value.
    :type min_selection: int
    :param max_selection: (int) - The maximum valid selection value.
    :type max_selection: int

    :return: (None) - returns None.
    :rtype: None
    """

    def __init__(self, message: str, min_selection: int, max_selection: int) -> None:
        super(InvalidChoiceError, self).__init__(message)
        self.min_selection: int = min_selection
        self.max_selection: int = max_selection


class InvalidInputError(LMSError):
    """
    Exception raised for invalid input errors in CLI inputs.

    :param message: (str) - The error message describing the invalid input.
    :type message: str
    :param validation_fn: (Callable) - The validation function used.
    :type validation_fn: Callable
    :param parsing_to: (str) - The type to which input was attempted to be parsed.
    :type parsing_to: str

    :return: (None) - returns None.
    :rtype: None
    """

    def __init__(self, message: str, validation_fn: Callable, parsing_to: str) -> None:
        super(InvalidInputError, self).__init__(message)
        self.validation_fn: Callable = validation_fn
        self.parsing_to: str = parsing_to


class InvalidSelectionInputError(LMSError):
    """
    Exception raised for invalid selection input errors in CLI inputs.

    :param message: (str) - The error message describing the invalid selection input.
    :type message: str

    :return: (None) - returns None.
    :rtype: None
    """

    def __init__(self, message: str) -> None:
        super(InvalidSelectionInputError, self).__init__(message)


class InvalidPathError(LMSError):
    """
    Exception raised for invalid path errors in CLI inputs.

    :param message: (str) - The error message describing the invalid path.
    :type message: str

    :return: (None) - returns None.
    :rtype: None
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


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

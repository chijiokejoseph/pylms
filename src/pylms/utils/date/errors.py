from pylms.errors import LMSError


class InvalidDateError(LMSError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class DateCourseMismatchError(LMSError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class CaseUnreachableError(LMSError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

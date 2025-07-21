from pylms.errors import LMSError


class NoClassFormError(LMSError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PathNotFoundError(LMSError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CaseUnreachableError(LMSError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

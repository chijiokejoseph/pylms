from pylms.errors import LMSError


class NoClassFormError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


class PathNotFoundError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


class CaseUnreachableError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)

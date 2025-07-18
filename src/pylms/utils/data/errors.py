from typing import Literal

from pylms.errors import LMSError

type ReadErrorType = Literal["FileNotFoundError", "PermissionError"]


class ReadError(LMSError):
    def __init__(self, kind: ReadErrorType, message: str) -> None:
        self.kind: ReadErrorType = kind
        self.message: str = message
        super().__init__(message)


class ValidationError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)

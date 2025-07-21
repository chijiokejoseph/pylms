from typing import Literal

from pylms.errors import LMSError

type ReadErrorType = Literal["FileNotFoundError", "PermissionError"]


class ReadError(LMSError):
    def __init__(self, kind: ReadErrorType, message: str) -> None:
        super().__init__(message)
        self.kind: ReadErrorType = kind


class ValidationError(LMSError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

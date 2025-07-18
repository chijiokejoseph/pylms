from pylms.errors import LMSError
from typing import Literal


type FormServiceType = Literal["create", "setup", "share"]


class FormServiceError(LMSError):
    def __init__(self, kind: FormServiceType, message: str) -> None:
        self.kind: FormServiceType = kind
        self.message: str = message
        super().__init__(message)

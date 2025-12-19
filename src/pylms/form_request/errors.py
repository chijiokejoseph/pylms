from typing import Literal

from ..errors import LMSError

type FormServiceType = Literal["create", "setup", "share"]


class FormServiceError(LMSError):
    def __init__(self, kind: FormServiceType, message: str) -> None:
        super().__init__(message)
        self.kind: FormServiceType = kind

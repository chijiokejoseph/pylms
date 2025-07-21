from pylms.errors import LMSError


class FilePermissionError(LMSError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        

class ShutilOpsError(LMSError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
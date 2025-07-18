from pylms.errors import LMSError


class NetworkError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)


class InvalidRetrieveArgsError(LMSError):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)

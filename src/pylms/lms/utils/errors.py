from pylms.errors import LMSError


class BadArgumentErr(LMSError):
    def __init__(self, msg: str) -> None:
        self.message: str = msg
        super().__init__(self.message)

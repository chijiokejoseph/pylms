from pylms.errors import LMSError


class BadArgumentErr(LMSError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

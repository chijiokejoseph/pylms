from pylms.errors import LMSError


class HasDuplicatesErr(LMSError):
    def __init__(self, msg: str):
        self.message: str = msg
        super().__init__(self.message)


class MissingColsErr(LMSError):
    def __init__(self, msg: str):
        self.message: str = msg
        super().__init__(self.message)

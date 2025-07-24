from pylms.errors import LMSError


class HasDuplicatesErr(LMSError):
    def __init__(self, msg: str):
        super().__init__(msg)


class MissingColsErr(LMSError):
    def __init__(self, msg: str):
        super().__init__(msg)

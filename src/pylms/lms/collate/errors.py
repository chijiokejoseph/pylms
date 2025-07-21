from pylms.errors import LMSError


class CollateIncompleteErr(LMSError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class SpreadSheetFmtErr(LMSError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class NoProjectGroupsErr(LMSError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class NonExistentPathErr(LMSError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class IntConvertErr(LMSError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class GradingRatioErr(LMSError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

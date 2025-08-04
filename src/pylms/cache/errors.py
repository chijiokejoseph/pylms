from pylms.errors import LMSError


class FilePermissionError(LMSError):
    """
    Exception raised for file permission errors in cache operations.

    :param message: (str) - The error message describing the permission issue.
    :type message: str

    :return: (None) - returns None.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        


class ShutilOpsError(LMSError):
    """
    Exception raised for errors during shutil operations in cache handling.

    :param message: (str) - The error message describing the shutil operation failure.
    :type message: str

    :return: (None) - returns None.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)

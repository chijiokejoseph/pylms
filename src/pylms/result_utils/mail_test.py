import unittest
from typing import final, override

from dotenv import load_dotenv

from ..data_service import load
from .mail import mail_result


@final
class TestSendResult(unittest.TestCase):
    """
    Unit test case for the send_result function.

    This class contains test methods to verify the behavior of the send_result function.

    :cvar None: (None) - No class variables are defined.
    """

    @override
    def setUp(self) -> None:
        _ = load_dotenv()
        self.ds = load()  # pyright: ignore[reportUninitializedInstanceVariable]

    def test_send_result(self) -> None:
        """
        Test the send_result function.

        This method calls the send_result function to ensure it executes without raising any exceptions.
        Additional assertions can be added to verify the expected outcomes of the function.

        :return: (None) - This test does not return a value.
        :rtype: None
        :raises Exception: (Exception) - If send_result raises an unexpected exception.
        """
        ds = self.ds.unwrap()
        _ = mail_result(ds).unwrap()


if __name__ == "__main__":
    _ = unittest.main()

import unittest
from typing import final, override

from dotenv import load_dotenv

from ..config import init_config
from ..data_service import load_ds
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
        self.config = init_config().unwrap()
        self.ds = load_ds(self.config).unwrap()

    def test_send_result(self) -> None:
        """
        Test the send_result function.

        This method calls the send_result function to ensure it executes without raising any exceptions.
        Additional assertions can be added to verify the expected outcomes of the function.

        :return: (None) - This test does not return a value.
        :rtype: None
        :raises Exception: (Exception) - If send_result raises an unexpected exception.
        """
        _ = mail_result(self.config, self.ds).unwrap()


if __name__ == "__main__":
    _ = unittest.main()

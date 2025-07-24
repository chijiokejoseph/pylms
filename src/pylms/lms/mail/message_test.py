import unittest
from pylms.lms.mail.message import send_result


class TestSendResult(unittest.TestCase):
    """
    Unit test case for the send_result function.

    This class contains test methods to verify the behavior of the send_result function.

    :cvar None: (None) - No class variables are defined.
    """

    def setUp(self) -> None:
        from dotenv import load_dotenv
        from pylms.data_ops import load

        load_dotenv()
        self.ds = load()

    def test_send_result(self) -> None:
        """
        Test the send_result function.

        This method calls the send_result function to ensure it executes without raising any exceptions.
        Additional assertions can be added to verify the expected outcomes of the function.

        :return: (None) - This test does not return a value.
        :rtype: None
        :raises Exception: (Exception) - If send_result raises an unexpected exception.
        """
        send_result(self.ds)


if __name__ == "__main__":
    unittest.main()

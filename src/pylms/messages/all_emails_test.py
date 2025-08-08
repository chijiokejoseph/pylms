import unittest
from pylms.history.history import History
from pylms.messages.all_emails import assessment_message_all, custom_message_all
from pylms.errors import Result, Unit
from pylms.data_ops.load import load
from pylms.utils import DataStore

from dotenv import load_dotenv


class AllEmailsTest(unittest.TestCase):
    """
    Unit test class for testing the email sending functionality to all recipients.

    :return: (None) - This test does not return a value.
    :rtype: None

    This test class sets up the necessary environment and data store, and includes tests
    to verify that the message_all_emails function executes successfully without errors.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by loading environment variables and initializing the data store.

        :return: (None) - This setup method does not return a value.
        :rtype: None
        """
        # Load environment variables from .env file
        load_dotenv()
        # Load the data store for use in tests
        self.ds: DataStore = load()
        # Load History
        self.history: History = History.load()

    def test_custom_message_all(self) -> None:
        """
        Test the message_all_emails function to ensure it sends emails to all recipients successfully.

        :return: (None) - This test method does not return a value.
        :rtype: None

        This test calls the message_all_emails function with the loaded data store and asserts
        that the result unwraps without exceptions, indicating success.
        """
        # Call the custom_message_all_emails function with the data store
        result: Result[Unit] = custom_message_all(self.ds)
        # Print error message if Result contains error
        if result.is_err():
            print(f"{result.error = }")
        # Assert that the result is successful and unwrap without error
        result.unwrap()

    def test_assessment_message_all(self) -> None:
        # Call the custom_message_all_emails function with the data store
        result: Result[Unit] = assessment_message_all(self.ds, self.history)
        # Print error message if Result contains error
        if result.is_err():
            print(f"{result.error = }")
        # Assert that the result is successful and unwrap without error
        result.unwrap()

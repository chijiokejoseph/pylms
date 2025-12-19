import unittest
from typing import final, override

from dotenv import load_dotenv

from pylms.data_service import load
from pylms.errors import Result, Unit
from pylms.history import load_history
from pylms.messages import assessment_message_all, custom_message_all


@final
class AllEmailsTest(unittest.TestCase):
    """
    Unit test class for testing the email sending functionality to all recipients.

    :return: (None) - This test does not return a value.
    :rtype: None

    This test class sets up the necessary environment and data store, and includes tests
    to verify that the message_all_emails function executes successfully without errors.
    """

    @override
    def setUp(self) -> None:
        """
        Set up the test environment by loading environment variables and initializing the data store.

        :return: (None) - This setup method does not return a value.
        :rtype: None
        """
        # Load environment variables from .env file
        _ = load_dotenv()
        # Load the data store for use in tests
        self.ds = load()  # pyright: ignore [reportUninitializedInstanceVariable]
        # Load History
        self.history = load_history()  # pyright: ignore [reportUninitializedInstanceVariable]

    def test_custom_message_all(self) -> None:
        """
        Test the message_all_emails function to ensure it sends emails to all recipients successfully.

        :return: (None) - This test method does not return a value.
        :rtype: None

        This test calls the message_all_emails function with the loaded data store and asserts
        that the result unwraps without exceptions, indicating success.
        """
        # Call the custom_message_all_emails function with the data store
        ds = self.ds.unwrap()
        result: Result[Unit] = custom_message_all(ds)
        # Print error message if Result contains error
        if result.is_err():
            print(f"{result.error = }")
        # Assert that the result is successful and unwrap without error
        _ = result.unwrap()

    def test_assessment_message_all(self) -> None:
        ds = self.ds.unwrap()
        history = self.history.unwrap()
        # Call the custom_message_all_emails function with the data store
        result: Result[Unit] = assessment_message_all(ds, history)
        # Print error message if Result contains error
        if result.is_err():
            print(f"{result.error = }")
        # Assert that the result is successful and unwrap without error
        _ = result.unwrap()

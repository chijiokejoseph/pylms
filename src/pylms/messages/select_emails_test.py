import unittest
from pylms.messages.select_emails import _message_select_emails
from pylms.messages.select_msg_builders import build_update_form_msg
from pylms.messages.message_record import MessageRecord
from pylms.email import run_email
from pylms.history import History
from pylms.errors import Result, Unit
from smtplib import SMTP
from dotenv import load_dotenv


class SelectEmailsTest(unittest.TestCase):
    """
    Unit test class for the message_select_emails function.

    This test class sets up the environment and includes a test to verify that the
    message_select_emails function executes successfully and returns a successful result.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by loading environment variables.

        :return: (None) - This setup method does not return a value.
        :rtype: None
        """
        # load environment
        load_dotenv()
        
        self.history: History = History.load()

    def test_message_select_emails(self) -> None:
        """
        Test the message_select_emails function to ensure it executes and returns a successful result.

        :return: (None) - This test method does not return a value.
        :rtype: None

        This test calls the message_select_emails function and asserts that the result indicates success.
        """

        # Inform about the test steps for different email input modes
        print("Run the test for each mode of providing email input")
        print("Modes tested: By csv, By txt, By xlsx, and By user input")
        print()

        def mock_fn(server: SMTP) -> Result[Unit]:
            """
            Mock function to test sending emails using different input modes.

            :param server: (SMTP) - The SMTP server instance used to send emails.
            :type server: SMTP

            :return: (Result[Unit]) - Result indicating overall success or failure of sending emails.
            :rtype: Result[Unit]

            This function calls the email sending function multiple times, simulating different
            input modes (csv, txt, xlsx, user input). It collects the results and returns success
            only if all sends succeed, otherwise aggregates and returns errors.
            """
            # Initialize a list to store the results of sending emails
            results: list[Result[Unit]] = []
            
            def builder() -> Result[list[MessageRecord]]:
                """
                Build update form messages from the test history.

                :return: (Result[list[MessageRecord]]) - Result containing a list of MessageRecord objects.
                :rtype: Result[list[MessageRecord]]

                This function calls the build_update_form_msg function with the test history to generate
                the messages to be sent in the test.
                """
                return build_update_form_msg(self.history)
            
            for _ in range(4):
                # Call the function under test for each input mode
                result: Result[Unit] = _message_select_emails(server, builder)
                # Print any error encountered during sending
                print(f"{result.error = }")
                # Append the result to the list
                results.append(result)
            # Return success only if all sends were successful
            if all(result.is_ok() for result in results):
                return Result[Unit].unit()
            else:
                # Aggregate errors if any send failed
                return Result[Unit].err(
                    ValueError(
                        "\n"
                        + "\n".join([str(result.error) for result in results])
                        + "\n"
                    )
                )

        # Assert that the result is a successful Result
        result = run_email(mock_fn)

        print(f"{result.error = }")
        self.assertTrue(result.is_ok())


if __name__ == "__main__":
    unittest.main()

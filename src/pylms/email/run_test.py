import unittest
from smtplib import SMTP
from pylms.email.run import run_email, must_get_env
from dotenv import load_dotenv


class RunEmailTest(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        
    def test_run_email(self) -> None:
        """
        Test the run_email function by passing a mock mail function that verifies an email address.

        :return: (None) - This method does not return a value.
        :rtype: None
        """
        def mock_mail_fn(smtp: SMTP) -> None:
            """
            Mock mail function that retrieves an email address from the environment and verifies it using the provided SMTP instance.

            :param smtp: (SMTP) - The SMTP instance used to verify the email address.
            :type smtp: SMTP
            :return: (None) - This function does not return a value.
            :rtype: None
            """
            email: str = must_get_env("EMAIL")
            smtp.verify(email)

        run_email(mock_mail_fn)


if __name__ == "__main__":
    unittest.main()

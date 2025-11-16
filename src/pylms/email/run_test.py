import unittest
from smtplib import SMTP
from typing import override

from dotenv import load_dotenv

from pylms.email.run import run_email
from pylms.errors import Result, Unit
from pylms.utils import must_get_env


class RunEmailTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        _ = load_dotenv()

    def test_run_email(self) -> None:
        """
        Test the run_email function by passing a mock mail function that verifies an email address.

        :return: (None) - This method does not return a value.
        :rtype: None
        """

        def mock_mail_fn(smtp: SMTP) -> Result[Unit]:
            """
            Mock mail function that retrieves an email address from the environment and verifies it using the provided SMTP instance.

            :param smtp: (SMTP) - The SMTP instance used to verify the email address.
            :type smtp: SMTP
            :return: (Result[Unit]) - This function does not return a value.
            :rtype: Result[Unit]
            """
            email: str = must_get_env("EMAIL")
            try:
                _ = smtp.verify(email)
                return Result.unit()
            except Exception as e:
                return Result[Unit].err(e)

        result = run_email(mock_mail_fn)
        if result.is_ok():
            print("Email sent successfully.")
        else:
            print(f"Failed to send email: {result.unwrap_err()}")


if __name__ == "__main__":
    _ = unittest.main()

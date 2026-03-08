import unittest
from smtplib import SMTP
from typing import override

from dotenv import load_dotenv

from pylms.constants import CONFIG_PATH

from ..errors import Result, Unit
from .run import run_email
from ..config import load_config


class RunEmailTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        _ = load_dotenv()

    def test_run_email(self) -> None:
        """Test run_email function with mock mail function that verifies email address.

        Uses a mock function to verify email address through SMTP connection
        and tests the run_email wrapper functionality.
        """

        config = load_config(CONFIG_PATH).unwrap()

        def mock_mail_fn(smtp: SMTP) -> Result[Unit]:
            """Mock mail function that verifies email address using SMTP.

            Args:
                smtp (SMTP): SMTP instance for email verification.

            Returns:
                Result[Unit]: Success or error from verification.
            """
            email: str = config.admin
            try:
                _ = smtp.verify(email)
                return Result.unit()
            except Exception as e:
                return Result[Unit].err(e)

        result = run_email(config, mock_mail_fn)
        if result.is_ok():
            print("Email sent successfully.")
        else:
            print(f"Failed to send email: {result.unwrap_err()}")


if __name__ == "__main__":
    _ = unittest.main()

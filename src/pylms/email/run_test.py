import unittest
from smtplib import SMTP
from typing import override

from dotenv import load_dotenv

from ..errors import Result, Unit
from ..paths import must_get_env
from .run import run_email


class RunEmailTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        _ = load_dotenv()

    def test_run_email(self) -> None:
        """Test run_email function with mock mail function that verifies email address.
        
        Uses a mock function to verify email address through SMTP connection
        and tests the run_email wrapper functionality.
        """
        def mock_mail_fn(smtp: SMTP) -> Result[Unit]:
            """Mock mail function that verifies email address using SMTP.
            
            Args:
                smtp (SMTP): SMTP instance for email verification.
                
            Returns:
                Result[Unit]: Success or error from verification.
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

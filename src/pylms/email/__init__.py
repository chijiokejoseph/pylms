from smtplib import SMTP, SMTPException
from typing import Callable
from pylms.constants import ENV_PATH
from pylms.errors import LMSError
import os


def must_get_env(variable: str) -> str:
    """
    Retrieve the value of an environment variable or raise an error if not set.

    :param variable: (str) - The name of the environment variable to retrieve.
    :type variable: str
    :return: (str) - The value of the environment variable.
    :rtype: str
    :raises LMSError: If the .env file does not exist or the variable is not set.
    """
    # Attempt to get the environment variable value
    value: str | None = os.getenv(variable)

    # If the variable is not set
    if value is None:
        # Check if the .env file exists
        if not ENV_PATH.exists():
            # Raise an error if the .env file does not exist
            raise LMSError(
                "The .env file does not exist. Please create it and try again"
            )

        # Raise an error if the variable is not set in the .env file
        raise LMSError(
            "The 'EMAIL' variable is not set in the .env file. Please set it and try again"
        )

    # Return the value of the environment variable
    return value


def run_email(mail_fn: Callable[[SMTP], None]) -> None:
    """
    Establish an SMTP connection, authenticate, execute a mail function, and close the connection.

    :param mail_fn: (Callable[[SMTP], None]) - A function that takes an SMTP object and performs email operations.
    :type mail_fn: Callable[[SMTP], None]

    :return: (None) - returns nothing
    :rtype: None

    :raises LMSError: If required environment variables are missing or authentication fails.
    """
    # Retrieve the sender's email address from environment variables
    email: str = must_get_env("EMAIL")

    # Retrieve the sender's email password from environment variables
    password: str = must_get_env("PASSWORD")

    server: SMTP | None = None
    try:
        # Create an SMTP connection to Gmail's SMTP server on port 587
        server = SMTP("smtp.gmail.com", 587)

        # Upgrade the connection to a secure TLS connection
        server.starttls()

        # Log in to the SMTP server using the provided credentials
        server.login(email, password)

        # Execute the provided mail function, passing the authenticated SMTP server object
        mail_fn(server)
    except SMTPException as e:
        # Raise a custom error if any SMTP-related exception occurs
        raise LMSError(f"SMTP error: {e}")
    finally:
        if server is None:
            # If the server was never created, exit the function
            return
        # Close the SMTP connection to free resources
        server.quit()


__all__ = ["run_email"]

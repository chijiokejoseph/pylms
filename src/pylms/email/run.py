from smtplib import SMTP, SMTP_SSL, SMTPException
from typing import Callable

from ..errors import Result, Unit
from ..paths import must_get_env

# Define the type for a mail error
type MailError = dict[str, tuple[int, bytes]]


def run_email(mail_fn: Callable[[SMTP], Result[Unit]]) -> Result[Unit]:
    """
    Establish an SMTP connection, authenticate, execute a mail function, and close the connection.

    :param mail_fn: (Callable[[SMTP], Result[Unit]]) - A function that takes an SMTP object and performs email operations.
    :type mail_fn: Callable[[SMTP], Result[Unit]]

    :return: (Result[Unit]) - returns a Result object indicating success or failure.
    :rtype: Result[Unit]
    """
    # Retrieve the sender's email address from environment variables
    email: str = must_get_env("EMAIL")

    # Retrieve the sender's email password from environment variables
    password: str = must_get_env("PASSWORD")

    server: SMTP | None = None
    try:
        # Create an SMTP connection to Gmail's SMTP server on port 587 using STARTTLS
        server = SMTP("smtp.gmail.com", 587)

        # Disable debug logging
        server.set_debuglevel(False)

        # Start TLS encryption
        _ = server.starttls()

        # Log in to the SMTP server using the provided credentials
        _ = server.login(email, password)

        # Execute the provided mail function, passing the authenticated SMTP server object
        _ = mail_fn(server)
        return Result[Unit].unit()
    except (TimeoutError, SMTPException):
        # Create an SMTP connection to Gmail's SMTP server on port 465 using SSL
        server = SMTP_SSL("smtp.gmail.com", 465)

        # Disable debug logging
        server.set_debuglevel(False)

        # Log in to the SMTP server using the provided credentials
        _ = server.login(email, password)

        # Execute the provided mail function, passing the authenticated SMTP server object
        _ = mail_fn(server)
        return Result[Unit].unit()
    except Exception as e:
        # Raise a custom error if any SMTP-related exception occurs
        return Result[Unit].err(e)
    finally:
        # Close the SMTP connection to free resources
        if server is not None and server.sock is not None:
            _ = server.quit()

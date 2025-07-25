from smtplib import SMTP, SMTP_SSL
from typing import Callable
from pylms.errors import Result
from pylms.utils import must_get_env


def run_email(mail_fn: Callable[[SMTP], Result[None]]) -> Result[None]:
    """
    Establish an SMTP connection, authenticate, execute a mail function, and close the connection.

    :param mail_fn: (Callable[[SMTP], Result[None]]) - A function that takes an SMTP object and performs email operations.
    :type mail_fn: Callable[[SMTP], Result[None]]

    :return: (Result[None]) - returns a Result object indicating success or failure.
    :rtype: Result[None]
    """
    # Retrieve the sender's email address from environment variables
    email: str = must_get_env("EMAIL")

    # Retrieve the sender's email password from environment variables
    password: str = must_get_env("PASSWORD")

    server: SMTP | None = None
    try:
        # Create an SMTP connection to Gmail's SMTP server on port 587
        server = SMTP_SSL("smtp.gmail.com", 465)

        # Disable debug logging
        server.set_debuglevel(False)

        # Log in to the SMTP server using the provided credentials
        server.login(email, password)

        # Execute the provided mail function, passing the authenticated SMTP server object
        mail_fn(server)
        return Result.ok(None)
    except Exception as e:
        # Raise a custom error if any SMTP-related exception occurs
        return Result[None].err(e)
    finally:
        # Close the SMTP connection to free resources
        if server is not None:
            server.quit()

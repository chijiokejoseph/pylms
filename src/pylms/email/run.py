from smtplib import SMTP, SMTP_SSL, SMTPException
from typing import Callable

from ..errors import Result, Unit
from ..paths import must_get_env

# Define the type for a mail error
type MailError = dict[str, tuple[int, bytes]]


def run_email(mail_fn: Callable[[SMTP], Result[Unit]]) -> Result[Unit]:
    """Establish SMTP connection, authenticate, execute mail function, and close connection.
    
    Args:
        mail_fn (Callable[[SMTP], Result[Unit]]): Function that performs email operations
            using the authenticated SMTP object.
            
    Returns:
        Result[Unit]: Success or error message from email operation.
    """
    # Retrieve email credentials from environment variables
    email: str = must_get_env("EMAIL")
    password: str = must_get_env("PASSWORD")

    server: SMTP | None = None
    try:
        # Create SMTP connection to Gmail on port 587 with STARTTLS
        server = SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(False)
        _ = server.starttls()
        _ = server.login(email, password)

        # Execute the mail function with authenticated server
        _ = mail_fn(server)
        return Result.unit()
    except (TimeoutError, SMTPException):
        # Fallback to SSL connection on port 465
        server = SMTP_SSL("smtp.gmail.com", 465)
        server.set_debuglevel(False)
        _ = server.login(email, password)
        _ = mail_fn(server)
        return Result.unit()
    except Exception as e:
        return Result.err(e)
    finally:
        # Close SMTP connection to free resources
        if server is not None and server.sock is not None:
            _ = server.quit()

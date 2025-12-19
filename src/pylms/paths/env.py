import os

from ..constants import ENV_PATH
from ..errors import LMSError


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

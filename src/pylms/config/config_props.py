from pylms.config.config import Config
from pylms.config.io import read_config
from pylms.errors import LMSError


def read_course_name() -> str:
    """
    Read the course name from the configuration.

    :return: (str) - The course name.
    :rtype: str
    :raises LMSError: If the course name is not set in the configuration.
    """
    # Read the configuration object
    toml: Config = read_config()

    # Check if the course name is set
    if not toml.has_course_name():
        raise LMSError("Course name not set")

    # Return the course name from the settings
    return toml.settings.course_name


def read_data_dir() -> str:
    """
    Read the data directory path from the configuration.

    :return: (str) - The data directory path.
    :rtype: str
    :raises LMSError: If the data directory is not set in the configuration.
    """
    # Read the configuration object
    toml: Config = read_config()

    # Check if the data directory is set
    if not toml.has_data_dir():
        raise LMSError("Data directory not set")

    # Return the data directory path from the settings
    return toml.settings.data_dir


def read_open() -> bool:
    """
    Read the 'open' state flag from the configuration.

    :return: (bool) - The open state flag.
    :rtype: bool
    :raises LMSError: If the open state is not set in the configuration.
    """
    # Read the configuration object
    toml: Config = read_config()

    # Check if the open state list is empty
    if len(toml.state.open) == 0:
        raise LMSError("Open not set")

    # Return the first element of the open state list
    return toml.state.open[0]

from ..errors import Result, eprint
from .config import Config
from .io import read_config


def read_course_name() -> Result[str]:
    """
    Read the course name from the configuration.

    :return: (str) - The course name.
    :rtype: str
    """
    # Read the configuration object
    toml: Config = read_config()

    # Check if the course name is set
    if not toml.has_course_name():
        msg = "Course name not set"
        eprint(msg)
        return Result.err(msg)

    # Return the course name from the settings
    return Result.ok(toml.settings.course_name)


def read_data_dir() -> Result[str]:
    """
    Read the data directory path from the configuration.

    :return: (str) - The data directory path.
    :rtype: str
    """
    # Read the configuration object
    toml: Config = read_config()

    # Check if the data directory is set
    if not toml.has_data_dir():
        msg = "Data directory not set"
        eprint(msg)
        return Result.err(msg)

    # Return the data directory path from the settings
    return Result.ok(toml.settings.data_dir)


def read_open() -> Result[bool]:
    """
    Read the 'open' state flag from the configuration.

    :return: (bool) - The open state flag.
    :rtype: bool
    """
    # Read the configuration object
    toml: Config = read_config()

    # Check if the open state list is empty
    if len(toml.state.open) == 0:
        msg = "Open not set"
        eprint(msg)
        return Result.err(msg)

    # Return the first element of the open state list
    return Result.ok(toml.state.open[0])

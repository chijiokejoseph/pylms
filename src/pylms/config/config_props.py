from ..errors import Result, eprint
from .config import Config
from .functions import has_course_name, has_data_dir


def read_course_name(config: Config) -> Result[str]:
    """Return the configured course name from config.

    Args:
        config: Config instance.

    Returns:
        Result[str]: Ok(course_name) when a non-empty course name is present;
            Err(error_message) when the course name is not set.
    """
    if not has_course_name(config):
        msg = "Course name not set"
        eprint(msg)
        return Result.err(msg)

    return Result.ok(config.course_name)


def read_data_dir(config: Config) -> Result[str]:
    """Return the configured data directory path from config.

    Args:
        config: Config instance.

    Returns:
        Result[str]: Ok(data_dir) when a valid data directory is configured;
            Err(error_message) when the data directory is not set.
    """
    if not has_data_dir(config):
        msg = "Data directory not set"
        eprint(msg)
        return Result.err(msg)

    return Result.ok(config.data_dir)


def read_open(config: Config) -> Result[bool]:
    """Return the configured 'open' flag from config.

    Args:
        config: Config instance.

    Returns:
        Result[bool]: Ok(flag) when an open/closed flag is present;
            Err(error_message) when no state has been recorded.
    """
    if len(config.open) == 0:
        msg = "Open not set"
        eprint(msg)
        return Result.err(msg)

    return Result.ok(config.open[0])

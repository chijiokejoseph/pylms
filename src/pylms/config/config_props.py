from ..errors import Result, eprint
from .config import Config
from .io import read_config


def read_course_name() -> Result[str]:
    """Return the configured course name from persistent configuration.

    Loads the application's configuration from disk and returns the configured
    course name wrapped in a `Result`. If no course name has been set the
    function logs an error message and returns a failure `Result`.

    Returns:
        Result[str]: Ok(course_name) when a non-empty course name is present;
            Err(error_message) when the course name is not set.

    Examples:
        >>> res = read_course_name()
        >>> if res.is_ok():
        ...     print(res.unwrap())
    """
    # Read the configuration object. `read_config` handles file I/O and parsing.
    # Any exceptions (I/O or parsing) will propagate to the caller.
    toml: Config = read_config()

    # Check if the course name is set in the loaded configuration.
    # This is a lightweight presence check (non-empty string).
    if not toml.has_course_name():
        msg = "Course name not set"
        eprint(msg)
        # Returning a Result.err keeps the function's API consistent for callers.
        return Result.err(msg)

    # Return the course name from the settings wrapped in a successful Result.
    # Wrapping keeps error handling uniform across the codebase.
    return Result.ok(toml.settings.course_name)


def read_data_dir() -> Result[str]:
    """Return the configured data directory path from persistent configuration.

    Loads the application's configuration and returns the `data_dir` setting
    wrapped in a `Result`. If the data directory has not been configured or
    does not exist the function logs an error and returns a failure `Result`.

    Returns:
        Result[str]: Ok(data_dir) when a valid data directory is configured;
            Err(error_message) when the data directory is not set.

    Examples:
        >>> res = read_data_dir()
        >>> if res.is_ok():
        ...     print(res.unwrap())
    """
    # Read the configuration object from disk into memory.
    toml: Config = read_config()

    # The `has_data_dir` method performs a filesystem existence check and
    # verifies the configured path is not an empty string. If it returns False
    # we log and return an error Result so callers can handle the missing config.
    if not toml.has_data_dir():
        msg = "Data directory not set"
        eprint(msg)
        return Result.err(msg)

    # Return the validated data directory path as the successful Result value.
    return Result.ok(toml.settings.data_dir)


def read_open() -> Result[bool]:
    """Return the configured 'open' flag from persistent configuration.

    The function reads the configuration and returns the earliest recorded
    'open' flag (the function mirrors the existing behavior of returning the
    first element of the `state.open` list). If no open/closed state has been
    recorded the function logs an error and returns a failure `Result`.

    Returns:
        Result[bool]: Ok(flag) when an open/closed flag is present;
            Err(error_message) when no state has been recorded.

    Examples:
        >>> res = read_open()
        >>> if res.is_ok():
        ...     print('open' if res.unwrap() else 'closed')
    """
    # Load the configuration into memory. Errors propagate from `read_config`.
    toml: Config = read_config()

    # Defensive check: ensure there's at least one recorded state entry.
    # Historically this function returns the *first* element of the list; that
    # represents the earliest recorded flag in the existing data model.
    if len(toml.state.open) == 0:
        msg = "Open not set"
        eprint(msg)
        return Result.err(msg)

    # Return the earliest recorded 'open' flag. Keep this behavior to match
    # existing callers; if callers need the most recent state they should use
    # the appropriate Config APIs or modify this function explicitly.
    return Result.ok(toml.state.open[0])

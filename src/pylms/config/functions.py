from pathlib import Path

from .config import Config
from .facilitator import Facilitator


def is_open(config: Config) -> bool:
    """Return whether the most recent recorded state is open.

    Args:
        config: Config instance.

    Returns:
        bool: True if the latest recorded state is open, False otherwise.

    Raises:
        IndexError: If the state history is empty.
    """
    return config.open[-1]


def has_data_dir(config: Config) -> bool:
    """Determine whether a configured data directory exists.

    Args:
        config: Config instance.

    Returns:
        bool: True if data_dir points to an existing, non-empty path.
    """
    path = Path(config.data_dir)
    return path.exists() and path != Path("")


def has_course_name(config: Config) -> bool:
    """Return whether a course name has been configured.

    Args:
        config: Config instance.

    Returns:
        bool: True if course_name is a non-empty string.
    """
    return config.course_name != ""


def mark_open(config: Config) -> None:
    """Mark the configuration as open.

    Args:
        config: Config instance.
    """
    config.open.append(True)


def mark_closed(config: Config) -> None:
    """Mark the configuration as closed.

    Args:
        config: Config instance.
    """
    config.open.append(False)


def reset_data_dir(config: Config) -> None:
    """Clear the configured data directory.

    Args:
        config: Config instance.
    """
    config.data_dir = ""


def reset_course_name(config: Config) -> None:
    """Clear the configured course name.

    Args:
        config: Config instance.
    """
    config.course_name = ""


def add_facilitator(config: Config, facilitator: Facilitator) -> None:
    """Add a facilitator to the config.

    Args:
        config: Config instance.
        facilitator: Facilitator to add.
    """
    config.facilitators.append(facilitator)

def verify_name(name: str) -> bool:
    """Validate a name string.

    Checks whether the provided string is a valid name (non-empty after stripping).

    Args:
        name (str): The name to validate.

    Returns:
        bool: True if name is non-empty after stripping, False otherwise.
    """
    return len(name.strip()) > 0

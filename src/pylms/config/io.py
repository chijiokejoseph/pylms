import tomlkit

from ..constants import STATE_PATH
from .config import Config


def new_config() -> Config:
    """Create and persist a new default configuration.

    This function constructs a default `Config` object, marks it as open,
    writes it to the configured `STATE_PATH` on disk, and returns the instance.

    Returns:
        Config: The newly created and persisted configuration object.
    """
    app_config = Config.default()
    app_config.open()
    write_config(app_config)
    return app_config


def load() -> Config:
    """Load the application configuration from disk or create a new one.

    If the configuration file exists at `STATE_PATH` it is read and parsed.
    Otherwise a new default configuration is created, persisted, and returned.

    Returns:
        Config: The loaded or newly created configuration object.
    """
    return read_config() if STATE_PATH.exists() else new_config()


def read_config() -> Config:
    """Read and parse the configuration file from `STATE_PATH`.

    The file is read using UTF-8 encoding and parsed with `tomlkit`.
    The parsed document is converted into a `Config` instance via
    `Config.from_value`.

    Returns:
        Config: The configuration parsed from disk.

    Raises:
        OSError: If the file cannot be opened.
        tomlkit.exceptions.TOMLKitError: If parsing fails.
    """
    with STATE_PATH.open(mode="r", encoding="utf-8") as f:
        document = tomlkit.loads(f.read())
        app_config: Config = Config.from_value(document)
        return app_config


def write_config(config: Config) -> None:
    """Write a `Config` instance to `STATE_PATH` as TOML.

    The configuration is converted to a mapping with `config.to_dict()` and
    serialized with `tomlkit.dumps`. The serialized text is written to the
    `STATE_PATH` file using UTF-8 encoding.

    Args:
        config: The `Config` instance to serialize and write.

    Raises:
        OSError: If the file cannot be written.
    """
    config_dict = config.to_dict()
    with STATE_PATH.open(mode="w", encoding="utf-8") as f:
        toml_text: str = tomlkit.dumps(config_dict)  # pyright: ignore [reportUnknownMemberType]
        _ = f.write(toml_text)
        return None

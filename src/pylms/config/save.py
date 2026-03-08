import json
from pathlib import Path

from ..constants import CONFIG_JSON, CONFIG_PATH
from ..errors import Result, Unit
from .config import Config


def save_config(config: Config) -> Result[Unit]:
    """Save current config data to JSON file.

    Saves config data to both the main config file and the data directory config file.

    Args:
        config (Config): Config instance to save.

    Returns:
        Result[Unit]: Success or error message.
    """
    from ..paths import display_path

    data = {
        "data_dir": config.data_dir,
        "course_name": config.course_name,
        "open": list(config.open),
        "facilitators": [f.to_dict() for f in config.facilitators],
        "admin": config.admin,
        "encryption_key": config.encryption_key,
        "encrypted_password": config.encrypted_password
    }

    config_path = Path(config.data_dir) / CONFIG_JSON
    with config_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    display_path(config, "Config")
    return Result.unit()

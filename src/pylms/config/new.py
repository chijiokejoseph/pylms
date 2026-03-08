import json
from pathlib import Path

from ..errors import Result, eprint
from ..info import print_info
from .config import Config
from .config_path import get_config_path
from .facilitator import Facilitator
from .functions import mark_open
from .input import setup_new_config
from .save import save_config


def init_config() -> Result[Config]:
    """Initialize config data storage.

    If config.json exists, loads it. Otherwise creates new config and prompts
    for data_dir, course_name, and facilitators.

    Returns:
        Result[Config]: Success with Config instance or error message.
    """
    path = get_config_path()

    if path.is_err():
        return path.propagate()

    path = path.unwrap()

    if isinstance(path, Path) and path.exists():
        config = load_config(path)
        if config.is_err():
            return config.propagate()
        config = config.unwrap()
        print_info("Config has been loaded")
        return Result.ok(config)

    result = setup_new_config()
    if result.is_err():
        return result.propagate()
    config = result.unwrap()

    mark_open(config)
    print_info("App config records have just been initialized")

    result = save_config(config)
    if result.is_err():
        return result.propagate()

    return Result.ok(config)


def load_config(path: Path) -> Result[Config]:
    """Load config data from JSON file and initialize Config object.

    Returns:
        Result[Config]: Success with loaded Config instance or error message.
    """
    config = Config()

    if not path.exists():
        msg = f"path to config.json '{path}' does not exist"
        eprint(msg)
        return Result.err(msg)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        msg = "Invalid config data format."
        eprint(msg)
        return Result.err(msg)

    if "data_dir" in data:
        if not isinstance(data["data_dir"], str):
            msg = "data_dir must be a string."
            eprint(msg)
            return Result.err(msg)
        config.data_dir = data["data_dir"]

    if "course_name" in data:
        if not isinstance(data["course_name"], str):
            msg = "course_name must be a string."
            eprint(msg)
            return Result.err(msg)
        config.course_name = data["course_name"]

    if "open" in data:
        if not isinstance(data["open"], list):
            msg = "open must be a list of booleans."
            eprint(msg)
            return Result.err(msg)
        if len(data["open"]) > 0 and not all(
            isinstance(val, bool) for val in data["open"]
        ):
            msg = "All open values must be booleans."
            eprint(msg)
            return Result.err(msg)
        config.open = data["open"]

    if "facilitators" in data:
        if not isinstance(data["facilitators"], list):
            msg = "facilitators must be a list."
            eprint(msg)
            return Result.err(msg)
        for f_data in data["facilitators"]:
            facilitator = Facilitator.from_dict(f_data)
            if facilitator.is_err():
                return facilitator.propagate()
            config.facilitators.append(facilitator.unwrap())

    if "admin" in data:
        if not isinstance(data["admin"], str):
            msg = "admin must be a string."
            eprint(msg)
            return Result.err(msg)
        config.admin = data["admin"]

    if "encrypted_password" in data:
        if not isinstance(data["encrypted_password"], str):
            msg = "encrypted_password must be a string."
            eprint(msg)
            return Result.err(msg)
        config.encrypted_password = data["encrypted_password"]

    if "encryption_key" in data:
        if not isinstance(data["encryption_key"], str):
            msg = "encryption_key must be a string."
            eprint(msg)
            return Result.err(msg)
        config.encryption_key = data["encryption_key"]

    return Result.ok(config)

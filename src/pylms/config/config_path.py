import json
from pathlib import Path

from ..constants import CONFIG_JSON, CONFIG_PATH
from ..errors import Result, Unit


def get_config_path() -> Result[Path] | Result[Unit]:
    """read default config path to see if config has been initialized before
    Return `Result[Unit]` if not initialized else `Result[Path]` where the Path
    is gotten from the `data_dir` key of the `config.json` file
    stored at the default config path

    Returns:
        Result[Unit] | Result[Path]: Result containing `data_dir` if config has been initialized before or containing `Unit` if config not initialized. May also contain `Err` if any of the validations fails.
    """
    if not CONFIG_PATH.exists():
        return Result.unit()

    with CONFIG_PATH.open() as f:
        data: dict[str, str] = json.load(f)

    if len(data) == 0:
        msg = f"Corrupt Installation. {CONFIG_PATH} is empty"
        return Result.err(msg)

    if "data_dir" in data:
        return Result.ok(Path(data["data_dir"]) / CONFIG_JSON)

    return Result.err(f"Corrupt Installation. {CONFIG_PATH} missing data_dir")

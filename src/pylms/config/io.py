from pylms.config.config import Config
from pylms.constants import STATE_PATH
import tomlkit


def new_config() -> Config:
    app_config = Config.default()
    app_config.open()
    write_config(app_config)
    return app_config


def load() -> Config:
    return read_config() if STATE_PATH.exists() else new_config()


def read_config() -> Config:
    with STATE_PATH.open(mode="r", encoding="utf-8") as f:
        document = tomlkit.loads(f.read())
        app_config: Config = Config.from_value(document)
        return app_config


def write_config(config: Config) -> None:
    config_dict = config.to_dict()
    with STATE_PATH.open(mode="w", encoding="utf-8") as f:
        toml_text: str = tomlkit.dumps(config_dict)
        f.write(toml_text)
        return None

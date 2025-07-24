from pylms.config.app_config import AppConfig
from pylms.constants import STATE_PATH
import tomlkit


def new_state() -> AppConfig:
    app_state = AppConfig.default()
    app_state.open()
    write_state(app_state)
    return app_state


def load() -> AppConfig:
    return read_state() if STATE_PATH.exists() else new_state()


def read_state() -> AppConfig:
    with STATE_PATH.open(mode="r", encoding="utf-8") as f:
        document = tomlkit.loads(f.read())
        app_state: AppConfig = AppConfig.from_value(document)
        return app_state


def write_state(state: AppConfig) -> None:
    state_dict = state.to_dict()
    with STATE_PATH.open(mode="w", encoding="utf-8") as f:
        toml_text: str = tomlkit.dumps(state_dict)
        f.write(toml_text)
        return None

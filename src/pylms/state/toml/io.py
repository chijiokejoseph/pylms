from pylms.state.toml.app_toml import AppToml
from pylms.constants import STATE_PATH, GLOBAL_RECORD_PATH
import os
import tomlkit


def new_state() -> AppToml:
    app_state = AppToml.default()
    app_state.open()
    write_state(app_state)
    os.remove(str(GLOBAL_RECORD_PATH.absolute()))
    return app_state


def load() -> AppToml:
    return read_state() if STATE_PATH.exists() else new_state()


def read_state() -> AppToml:
    with STATE_PATH.open(mode="r", encoding="utf-8") as f:
        document = tomlkit.loads(f.read())
        app_state: AppToml = AppToml.from_value(document)
        return app_state


def write_state(state: AppToml) -> None:
    state_dict = state.to_dict()
    with STATE_PATH.open(mode="w", encoding="utf-8") as f:
        toml_text: str = tomlkit.dumps(state_dict)
        f.write(toml_text)
        return None

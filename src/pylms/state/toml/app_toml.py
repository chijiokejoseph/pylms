from typing import Any, Self, cast
from abc import ABC, abstractmethod
from pathlib import Path


class TomlProtocol(ABC):
    @classmethod
    @abstractmethod
    def default(cls) -> Self:
        pass

    @classmethod
    @abstractmethod
    def from_value(cls, value_in: Any) -> Self:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class TomlSettings(TomlProtocol):
    data_dir: str

    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir

    @classmethod
    def default(cls) -> Self:
        return cls(data_dir="")

    @classmethod
    def from_value(cls, value_in: Any) -> Self:
        default = cls(data_dir="")
        if not isinstance(value_in, dict):
            return default
        keys = list(value_in.keys())
        values = list(value_in.values())
        if len(keys) == 0:
            return default
        if len(values) == 0:
            return default
        key: Any = keys[0]
        value: Any = values[0]
        if key != "data_dir":
            return default
        if not isinstance(value, str):
            return default
        return cls(data_dir=value)

    def to_dict(self) -> dict[str, str]:
        return {"data_dir": self.data_dir}


class TomlState(TomlProtocol):
    open: list[bool]

    def __init__(self, open_in: list[bool]) -> None:
        self.open = open_in

    @classmethod
    def default(cls) -> Self:
        return cls(open_in=[])

    @classmethod
    def from_value(cls, value_in: Any) -> Self:
        default = cls(open_in=[])
        if not isinstance(value_in, dict):
            return default
        for key, value in value_in.items():
            if key != "open":
                continue
            if not isinstance(value, list):
                continue
            if len(value) == 0 or not isinstance(value[0], bool):
                continue
            return cls(open_in=cast(list[bool], value))
        return default

    def to_dict(self) -> dict[str, list[bool]]:
        return {"open": self.open}


class AppToml(TomlProtocol):
    settings: TomlSettings
    state: TomlState

    def __init__(self, settings: TomlSettings, state: TomlState) -> None:
        self.settings = settings
        self.state = state

    @classmethod
    def default(cls) -> Self:
        return cls(settings=TomlSettings.default(), state=TomlState.default())

    @classmethod
    def from_value(cls, value_in: Any) -> Self:
        default = cls(settings=TomlSettings.default(), state=TomlState.default())
        if not isinstance(value_in, dict):
            return default
        for key, item in value_in.items():
            match str(key):
                case "settings":
                    default.settings = TomlSettings.from_value(item)
                case "state":
                    default.state = TomlState.from_value(item)
                case _:
                    pass

        return default

    def to_dict(self) -> dict:
        return {"settings": self.settings.to_dict(), "state": self.state.to_dict()}

    def is_open(self) -> bool:
        return self.state.open[-1]

    def has_data_dir(self) -> bool:
        path = Path(self.settings.data_dir)
        return path.exists() and path != Path("")

    def open(self) -> None:
        self.state.open.append(True)

    def close(self) -> None:
        self.state.open.append(False)

    def reset_data_dir(self) -> None:
        self.settings.data_dir = ""

    @property
    def data_dir(self) -> str:
        return self.settings.data_dir

    @property
    def open_(self) -> list[bool]:
        return self.state.open
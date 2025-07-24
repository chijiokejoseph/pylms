from pylms.config.app_config import AppConfig
from pylms.config.io import read_state
from pylms.errors import LMSError


def read_course_name() -> str:
    toml: AppConfig = read_state()
    if not toml.has_course_name():
        raise LMSError("Course name not set")
    return toml.settings.course_name


def read_data_dir() -> str:
    toml: AppConfig = read_state()
    if not toml.has_data_dir():
        raise LMSError("Data directory not set")
    return toml.settings.data_dir


def read_open() -> bool:
    toml: AppConfig = read_state()
    if len(toml.state.open) == 0:
        raise LMSError("Open not set")
    return toml.state.open[0]

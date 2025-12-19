from .config import Config
from .config_props import read_course_name, read_data_dir, read_open
from .io import load, new_config, read_config, write_config

__all__ = [
    "load",
    "new_config",
    "read_course_name",
    "read_data_dir",
    "read_open",
    "read_config",
    "write_config",
    "Config",
]

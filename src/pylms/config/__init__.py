from pylms.config.input_to_config import input_dir, input_course_name
from pylms.config.io import load, new_config, read_config, write_config
from pylms.config.config_props import read_course_name, read_data_dir, read_open
from pylms.config.config import Config

__all__ = [
    "load",
    "new_config",
    "input_dir",
    "input_course_name",
    "read_course_name",
    "read_data_dir",
    "read_open",
    "read_config",
    "write_config",
    "Config",
]

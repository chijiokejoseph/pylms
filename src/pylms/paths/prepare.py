from ..config import Config
from .path_fns import get_excel_path
from ..constants import DATA_PATH


def prepare_paths(config: Config) -> None:
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    get_excel_path(config).mkdir(parents=True, exist_ok=True)

from pylms.cli_utils import emphasis
from pylms.info import printpass
from pylms.paths import get_data_path, get_paths_excel

data_path = get_data_path()
ds_path = get_paths_excel()["DataStore"]
path_display = str(ds_path).replace(str(data_path), "...DATA")
path_display = emphasis(path_display)
printpass(f'DataStore saved at path "{path_display}"')

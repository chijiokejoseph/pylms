import unittest
from pathlib import Path
from typing import Literal

from pylms.utils import paths
from pylms.utils.paths.path_fns import get_paths_json


def get_update_path(path_type: Literal["form", "record"], timestamp: str) -> Path:
    if path_type == "form":
        return get_paths_json()["UpdateForm"] / f"{timestamp}_update_form.json"
    else:
        return get_paths_json()["UpdateRecord"] / f"{timestamp}_update_record.json"


def last_update_path(path_type: Literal["form", "record"], timestamp: str) -> Path:
    form_dir = (
        get_paths_json()["UpdateForm"]
        if path_type == "form"
        else get_paths_json()["UpdateRecord"]
    )
    items: list[Path] = list(form_dir.iterdir())
    if len(items) == 0:
        return get_update_path(path_type, timestamp)
    return items[-1]


def to_update_record(update_form_path: Path) -> Path:
    parent: Path = update_form_path.parent
    path_name = update_form_path.name
    new_path_name: str = path_name.replace("update_form", "update_record")
    return parent / new_path_name


def ret_update_path(timestamp: str) -> tuple[Path, Path]:
    update_form_path: Path = get_update_path("form", timestamp)
    update_record_path: Path = get_update_path("record", timestamp)
    if not update_form_path.exists():
        update_form_path = paths.last_update_path("form", timestamp)
        update_record_path = to_update_record(update_form_path)

    return update_form_path, update_record_path


class TestLastUpdate(unittest.TestCase):
    def setUp(self) -> None:
        from pylms.history import History

        self.history: History = History.load()

    def test_last_update(self):
        from pylms.forms.utils import select_form

        path = last_update_path("form", select_form(self.history, "update").timestamp)
        new_path = to_update_record(path)
        print(path)
        print(new_path)

    def test_ret_update(self):
        from pylms.forms.utils import select_form

        form_path, record_path = ret_update_path(
            select_form(self.history, "update").timestamp
        )
        print(f"{form_path = }")
        print(f"{record_path = }")


if __name__ == "__main__":
    unittest.main()

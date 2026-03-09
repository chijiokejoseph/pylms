from pathlib import Path
from unittest import TestCase
from pylms.paths import rm_path

def make(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

class TestRm(TestCase):
    def test_rm(self) -> None:
        data = "E:/Python/pylms/data"
        del_path = Path(data) / "del"
        make(del_path)
        for i in range(3):
            item_path = del_path / f"item{i}.txt"
            make(item_path)
            dir_path = del_path / f"dir{i}"
            make(dir_path)
            for j in range(3):
                subitem_path = dir_path / f"item{j}.csv"
                make(subitem_path)
        rm_path(del_path)
        self.assertFalse(del_path.exists())
        


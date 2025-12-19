from unittest import TestCase, main

from ..constants import STATE_PATH
from .io import new_config, read_config


class TestNew(TestCase):
    def test_new(self) -> None:
        _ = new_config()
        self.assertTrue(STATE_PATH.exists())

    def test_read(self) -> None:
        table = read_config()
        print(f"{table.state.open = }")
        self.assertTrue(table.settings.data_dir == "")
        self.assertTrue(table.state.open == [True])


if __name__ == "__main__":
    _ = main()

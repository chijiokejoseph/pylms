from unittest import TestCase, main
from pylms.config.io import read_config, new_config
from pylms.constants import STATE_PATH


class TestNew(TestCase):
    def test_new(self) -> None:
        new_config()
        self.assertTrue(STATE_PATH.exists())

    def test_read(self) -> None:
        table = read_config()
        print(f"{table.state.open = }")
        self.assertTrue(table.settings.data_dir == "")
        self.assertTrue(table.state.open == [True])


if __name__ == "__main__":
    main()

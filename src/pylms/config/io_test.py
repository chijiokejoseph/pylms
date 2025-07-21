from unittest import TestCase, main
from pylms.config.io import read_state, new_state
from pylms.constants import STATE_PATH


class TestNew(TestCase):
    def test_new(self) -> None:
        new_state()
        self.assertTrue(STATE_PATH.exists())

    def test_read(self) -> None:
        table = read_state()
        print(f"{table.state.open = }")
        self.assertTrue(table.settings.data_dir == "")
        self.assertTrue(table.state.open == [True])


if __name__ == "__main__":
    main()

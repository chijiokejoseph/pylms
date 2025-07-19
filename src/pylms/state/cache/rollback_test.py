import unittest
from unittest import TestCase

from pylms.data_ops import load
from pylms.state.cache.rollback import rollback_to_cmd
from pylms.utils import paths


class TestRollBack(TestCase):
    def setUp(self) -> None:
        self.ds = load()

    def tearDown(self) -> None:
        return None

    def test_copy_data(self) -> None:
        new_data_path = paths.get_data_path().parent / "test"
        new_data_path.mkdir(parents=True, exist_ok=True)
        rollback_to_cmd(new_data_path)


if __name__ == "__main__":
    unittest.main()
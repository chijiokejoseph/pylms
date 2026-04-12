from pylms.config import init_config
import unittest
from typing import final, override
from unittest import TestCase

from pylms import paths
from pylms.cache.rollback import rollback_to_cmd
from pylms.data_service import load_ds


@final
class TestRollBack(TestCase):
    """
    Unit test class for testing the rollback_to_cmd functionality.
    """

    @override
    def setUp(self) -> None:
        """
        Set up test environment by loading data.

        :return: (None) - returns None.
        :rtype: None
        """
        # Load the dataset before each test
        self.config = init_config().unwrap()
        self.ds = load_ds(self.config).unwrap()  

    @override
    def tearDown(self) -> None:
        """
        Tear down test environment. Currently does nothing.

        :return: (None) - returns None.
        :rtype: None
        """
        # No teardown actions needed currently
        return None

    def test_copy_data(self) -> None:
        """
        Test the rollback_to_cmd function by creating a test data path and invoking rollback.

        :return: (None) - returns None.
        :rtype: None
        """
        # Create a new directory for test data if it doesn't exist
        new_data_path = paths.get_data_path(self.config).parent / "test"
        new_data_path.mkdir(parents=True, exist_ok=True)
        # Call the rollback command with the test data path
        result = rollback_to_cmd(self.config, new_data_path)
        if result.is_err():
            return


if __name__ == "__main__":
    _ = unittest.main()

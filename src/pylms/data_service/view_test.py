from typing import final, override
from unittest import TestCase, main

from ..config import init_config
from .load import load_ds
from .view import view


@final
class ViewTest(TestCase):
    @override
    def setUp(self) -> None:
        config = init_config().unwrap()
        self.ds = load_ds(config)

    def test_view(self) -> None:
        ds = self.ds.unwrap()
        _ = view(ds).unwrap()


if __name__ == "__main__":
    _ = main()

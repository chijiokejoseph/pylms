from typing import final, override
from unittest import TestCase, main

from .edit import edit
from .load import load
from .view import view


@final
class EditTest(TestCase):
    @override
    def setUp(self) -> None:
        self.ds = load()  # pyright: ignore [reportUninitializedInstanceVariable]

    def test_edit(self) -> None:
        ds = self.ds.unwrap()
        _ = edit(ds).unwrap()
        _ = view(ds).unwrap()


if __name__ == "__main__":
    _ = main()

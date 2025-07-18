from unittest import TestCase, main
from pylms.data_ops.load import load
from pylms.data_ops.edit import edit
from pylms.data_ops.view import view


class EditTest(TestCase):
    def setUp(self) -> None:
        self.ds = load()

    def test_edit(self) -> None:
        self.ds = edit(self.ds)
        view(self.ds)


if __name__ == "__main__":
    main()
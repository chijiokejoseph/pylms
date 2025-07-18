from unittest import TestCase, main
from pylms.data_ops.load import load
from pylms.data_ops.view import view


class ViewTest(TestCase):
    def setUp(self) -> None:
        self.ds = load()

    def test_view(self) -> None:
        view(self.ds)


if __name__ == "__main__":
    main()
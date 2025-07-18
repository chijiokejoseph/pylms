from pathlib import Path
from unittest import TestCase, main

from pylms.utils.rm import rm_path


class RmTest(TestCase):
    def setUp(self) -> None:
        self.path = Path(__file__).parent / "house"
        self.path.mkdir(parents=True, exist_ok=True)
        print(f"{self.path = }")

    def test_rm_path(self) -> None:
        rm_path(self.path)
        self.assertFalse(self.path.exists())


if __name__ == "__main__":
    main()
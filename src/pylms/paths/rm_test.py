from pathlib import Path
from typing import final, override
from unittest import TestCase, main

from .rm import rm_path


@final
class RmTest(TestCase):
    @override
    def setUp(self) -> None:
        self.path = Path(__file__).parent / "house"  # pyright: ignore[reportUninitializedInstanceVariable]
        self.path.mkdir(parents=True, exist_ok=True)
        print(f"{self.path = }")

    def test_rm_path(self) -> None:
        _ = rm_path(self.path).unwrap()
        self.assertFalse(self.path.exists())


if __name__ == "__main__":
    _ = main()

import unittest
from typing import final, override

from .form_create import run_create_form


@final
class TestCreateForm(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.form_title = "Test Form Title"  # pyright: ignore[reportUninitializedInstanceVariable]
        self.form_name = "Test Form Name"  # pyright: ignore[reportUninitializedInstanceVariable]
        self.form_resource = None  # pyright: ignore[reportUninitializedInstanceVariable]

    def test_create_form(self) -> None:
        self.form_resource = run_create_form(
            form_title=self.form_title,
            form_name=self.form_name,
        )
        self.assertIsNotNone(self.form_resource)
        url = self.form_resource.url if self.form_resource is not None else None
        print(f"{url = }")


if __name__ == "__main__":
    _ = unittest.main()

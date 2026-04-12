import unittest
from typing import final, override

from .form_create import run_create_form
from ..models import Form


@final
class TestCreateForm(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.form_title: str = "Test Form Title"  
        self.form_name: str = "Test Form Name" 
        self.form_resource: Form | None = None

    def test_create_form(self) -> None:
        self.form_resource = run_create_form(
            form_title=self.form_title,
            form_name=self.form_name,
        ).unwrap()
        self.assertIsNotNone(self.form_resource)
        url = self.form_resource.url if self.form_resource is not None else None
        print(f"{url = }")


if __name__ == "__main__":
    _ = unittest.main()

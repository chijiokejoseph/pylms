import unittest

from pylms.models import Form
from pylms.forms.utils.service.form_create import create_form


class CreateFormTest(unittest.TestCase):
    def setUp(self) -> None:
        self.form_title = "Test Form Title"
        self.form_name = "Test Form Name"
        self.form_resource: Form | None = None

    def test_create_form(self) -> None:
        self.form_resource = create_form(
            form_title=self.form_title,
            form_name=self.form_name,
        )
        self.assertIsNotNone(self.form_resource)
        url = self.form_resource.url if self.form_resource is not None else None
        print(f"{url = }")


if __name__ == "__main__":
    unittest.main()
import unittest
from typing import final, override

from pylms.form_utils import select_form
from pylms.history import load_history
from pylms.paths import last_update_path, ret_update_path, to_update_record


@final
class TestLastUpdate(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.history = load_history()  # pyright: ignore [reportUninitializedInstanceVariable]

    def test_last_update(self) -> None:
        history = self.history.unwrap()
        path = last_update_path(
            "form", select_form(history, "update").unwrap().timestamp
        )
        new_path = to_update_record(path)
        print(path)
        print(new_path)

    def test_ret_update(self):
        history = self.history.unwrap()
        form_path, record_path = ret_update_path(
            select_form(history, "update").unwrap().timestamp
        )
        print(f"{form_path = }")
        print(f"{record_path = }")


if __name__ == "__main__":
    _ = unittest.main()

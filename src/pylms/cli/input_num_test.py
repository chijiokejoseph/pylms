from unittest import TestCase

from ..errors import Result, eprint
from ..info import print_info
from .custom_inputs import input_num


class TestInputs(TestCase):
    def test_input_num(self) -> None:
        value: Result[int] = input_num(
            "Enter your age: ",
            1,
        )
        if value.is_err():
            eprint(f"{value.unwrap_err()}")
            return
        age = value.unwrap()
        print_info(f"Your age is {age}")

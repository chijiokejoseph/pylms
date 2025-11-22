from unittest import TestCase

from pylms.cli.custom_inputs import input_num
from pylms.errors import Result, eprint
from pylms.info import println


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
        println(f"Your age is {age}")

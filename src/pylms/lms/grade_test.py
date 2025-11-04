from typing import override
from unittest import TestCase

from pylms.lms.grade import prepare_grading


class TestGradePy(TestCase):
    @override
    def setUp(self) -> None:
        return super().setUp()

    def test_prepare_grade(self) -> None:
        result = prepare_grading(10)
        assert result.is_ok(), (
            f"result failed because of the error {result.unwrap_err()}"
        )

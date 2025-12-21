from unittest import TestCase

from .new import load_history


class TestNew(TestCase):
    def test_load_history(self):
        _ = load_history().unwrap()

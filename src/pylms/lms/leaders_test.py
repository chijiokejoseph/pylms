from unittest import TestCase

from pylms.data_ops import load
from pylms.history.history import History
from pylms.lms import select_leaders
from pylms.lms.group import group


class TestSelectLeaders(TestCase):
    def test_select_leaders(self) -> None:
        ds = load()
        history = History.load()
        group(ds, history)
        _ = select_leaders(ds, history)

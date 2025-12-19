from unittest import TestCase

from pylms.data_service import load
from pylms.history import load_history
from pylms.lms import select_leaders
from pylms.lms.group import group


class TestSelectLeaders(TestCase):
    def test_select_leaders(self) -> None:
        ds = load().unwrap()
        history = load_history().unwrap()
        _ = group(ds, history).unwrap()
        _ = select_leaders(ds, history)

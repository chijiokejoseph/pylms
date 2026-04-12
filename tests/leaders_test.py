from unittest import TestCase

from pylms.config import init_config
from pylms.data_service import init_ds
from pylms.history import init_history
from pylms.lms import group, select_leaders


class TestSelectLeaders(TestCase):
    def test_select_leaders(self) -> None:
        config = init_config().unwrap()
        history = init_history(config).unwrap()
        ds = init_ds(config, history).unwrap()
        _ = group(config, ds, history).unwrap()
        _ = select_leaders(config, ds, history)

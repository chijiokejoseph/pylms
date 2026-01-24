from unittest import TestCase

from .new import load_history


class TestNew(TestCase):
    """Test cases for history loading functionality."""
    
    def test_load_history(self):
        """Test that history can be loaded without errors."""
        _ = load_history().unwrap()

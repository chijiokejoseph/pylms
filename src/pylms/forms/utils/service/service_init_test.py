import unittest

from pylms.forms.utils.service.service_init import _load_creds


class LoadCredsTest(unittest.TestCase):
    def test_load_creds(self) -> None:
        creds = _load_creds()
        self.assertIsNotNone(creds)


if __name__ == "__main__":
    unittest.main()
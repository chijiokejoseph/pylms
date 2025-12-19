import unittest

from .service_init import load_creds


class LoadCredsTest(unittest.TestCase):
    def test_load_creds(self) -> None:
        creds = load_creds()
        self.assertIsNotNone(creds)


if __name__ == "__main__":
    _ = unittest.main()

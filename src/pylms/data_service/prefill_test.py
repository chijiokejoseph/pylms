import unittest

from .prefill import prefill_ds


class PrefillTest(unittest.TestCase):
    def test_prefill_ds(self) -> None:
        ds = prefill_ds()
        print(ds.data)


if __name__ == "__main__":
    _ = unittest.main()

from pylms.data_ops.prefill import prefill_ds
import unittest


class PrefillTest(unittest.TestCase):
    def test_prefill_ds(self) -> None:
        ds = prefill_ds()
        print(ds.data)
        
        
if __name__ == "__main__":
    unittest.main()
    

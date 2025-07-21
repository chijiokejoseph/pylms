from pylms.utils.date.retrieve_dates import retrieve_dates
import unittest


class TestRetrieveDates(unittest.TestCase):
    def test_retrieve_dates(self) -> None:
        dates = retrieve_dates()
        print(f"{dates = }")
        
        
if __name__ == "__main__":
    unittest.main()
    


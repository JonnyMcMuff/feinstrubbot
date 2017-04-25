import unittest
from start import Feinstrubbot


class chainTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_parsing(self):
        handler_list_example = ['#1', '#2', '#3']
        #feinstrub object
        feinstrubbot = Feinstrubbot()
        #check if data is returned (is calling return sensors function) if string is longer then 500 signs data should be correct
        self.assertGreater( len(feinstrubbot.dataChain("recieve")), 500)

if __name__ == '__main__':
    unittest.main()

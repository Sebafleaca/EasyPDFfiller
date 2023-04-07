import unittest
import sys
from EasyPDFfiller import *


class TestEasyPDFfiller(unittest.TestCase):
    def test_open_file(self):
        self.assertIsNotNone(read_PDF)
    
    def test_num_of_pages(self):
        self.assertIsNot(num_pages, 0)
    
    def test_no_empty(self):
        self.assertIsNotNone(text)


if __name__ == '__main__':
    input_file = sys.argv[1]
    unittest.main(argv=[input_file])
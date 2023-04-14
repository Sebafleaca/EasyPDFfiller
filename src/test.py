import unittest
import sys
from pdfrw import PdfReader
from EasyPDFfiller import PdfFiller


class TestEasyPDFfiller(unittest.TestCase):

    def setUp(self) -> None:
        pdf_reader = PdfReader(sys.argv[1])
        self.filler = PdfFiller(pdf_reader, sys.argv[2])
        return super().setUp()

    def test_open_file(self):
        self.assertIsNotNone(self.filler)
    
    def test_num_of_pages(self):
        self.assertIsNotNone(self.filler)

    def test_filled_forms(self):
        filled_file = PdfReader(self.filler.get_output())
        page_1 = filled_file.pages[0]
        for annot in page_1['/Annots']:
            filled_form_value = annot['/V'][1:-1]
            sample_value = self.filler.data[annot['/T'][1:-1]]
            self.assertEqual(filled_form_value, str(sample_value))


if __name__ == '__main__':
    unittest.main(argv=[''])
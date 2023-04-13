import unittest
import pdfrw
from EasyPDFfiller import *


class TestEasyPDFfiller(unittest.TestCase):

    def test_open_file(self):
        self.assertIsNotNone(input_pdf)
    
    def test_num_of_pages(self):
        self.assertIsNotNone(pages)

    def test_filled_forms(self):
        filled_file = pdfrw.PdfReader("filled-sample.pdf")
        page_1 = filled_file.pages[0]
        for annot in page_1['/Annots']:
            filled_form_value = annot['/V'][1:-1]
            sample_value = data[annot['/T'][1:-1]]
            self.assertEqual(filled_form_value, str(sample_value))


if __name__ == '__main__':
    input_file = "fillable-sample.pdf"
    unittest.main(argv=[input_file])
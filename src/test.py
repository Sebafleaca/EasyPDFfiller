import unittest
import sys
from pdfrw import PdfReader
from EasyPDFfiller import PdfFiller


class TestEasyPDFfiller(unittest.TestCase):

    def setUp(self) -> None:
        pdf_reader = PdfReader(sys.argv[1])
        self.filler = PdfFiller(pdf_reader, sys.argv[2])
        return super().setUp()

    def test_filled_forms(self):
        if (sys.argv[1] == "resources/complex-sample.pdf"):
            if (sys.argv[2] == "resources/complex-data.json"):
                filled_file = PdfReader("resources/complex-filled.pdf")
                pages = filled_file.pages
                for page in pages:
                    for annot in page['/Annots']:
                        if annot['/FT'] == '/Tx':
                            filled_form_value = annot['/V'][1:-1]
                            sample_value = self.filler.data[annot['/T'][1:-1]]
                            self.assertEqual(filled_form_value, str(sample_value))

    def test_no_pages(self):
        if(sys.argv[1] == "resources/test/no-pages-pdf.pdf"):
            self.assertIn("PDF has no pages", self.filler.errors)

    def test_no_data(self):
        if(sys.argv[2] == "resources/test/no-data.json"):
            self.assertIn("Can't read JSON file", self.filler.errors)

    def test_empty_page(self):
        if(sys.argv[1] == "resources/test/empty-page.pdf"):
            self.assertIn("PDF's page is empty", self.filler.errors)

    def test_no_field_data(self):
        if(sys.argv[2] == "resources/test/wrong-data.json"):
            self.assertIn("Field name not in JSON data", self.filler.errors)

    def test_maxlen_exceeded(self):
        if(sys.argv[2] == "resources/test/wrong-data.json"):
            self.assertIn("Text field's MaxLen exceeded", self.filler.errors)


if __name__ == '__main__':
    unittest.main(argv=[''])

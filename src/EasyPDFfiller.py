import sys
from pdfrw import PdfReader, PdfWriter, PdfDict
import json


class PdfFiller:

    output_pdf = ""
    pages = []
    data = {}
    errors = []

    # Initialize a PdfFiller object.
    def __init__(self, input_pdf, data_file):
        self.input_pdf = input_pdf
        self.pages = input_pdf.pages
        if len(self.pages) <= 0:
            self.errors.insert("PDF has no pages")
        self.load_data(data_file)
        self.output_pdf = "resources/filled-sample.pdf"
        
    # Load data from json to dict.
    def load_data(self, data_in) -> None:
        with open(data_in, 'r') as json_file:
            self.data = json.load(json_file)
        if not self.data:
            self.errors.insert("No data in the JSON")
    
    # Form-filler procedure.
    def fill_forms(self) -> str:
        for page in self.pages:
            if page:
                for annot in page['/Annots']:
                    if annot['/T']:
                        data_to_fill = self.data[annot['/T'][1:-1]]
                        annot.update(PdfDict(V='{}'.format(data_to_fill)))
                        annot.update(PdfDict(Ff=1))
                    else:
                        self.errors.insert("Form's name is empty")
            else:
                self.errors.insert("PDF's page is empty")

        if len(self.errors) == 0:
            PdfWriter().write(self.output_pdf, self.input_pdf)
        else:
            print("Errors: " + self.errors)
            raise Exception("Errors encountered, writing not possible.")
        
        return str(self.output_pdf)


if len(sys.argv) != 3:
    raise Exception("Wrong number of arguments.\n" + 
        "Usage: python EasyPDFfiller.py pdf-file.pdf data-file.json")
if not sys.argv[1].endswith(".pdf"):
    raise Exception("First argument must be a PDF file.")
if not sys.argv[2].endswith(".json"):
    raise Exception("Second argument must be a JSON file.")

try:
    pdf_reader = PdfReader(sys.argv[1])
except:
    raise Exception("Can't read PDF file.")
try:
    data_file = sys.argv[2]
except:
    raise Exception("Can't read JSON file.")

fillerObject = PdfFiller(pdf_reader, data_file)
print(fillerObject.fill_forms())
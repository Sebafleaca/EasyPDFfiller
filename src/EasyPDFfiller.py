import sys
from pdfrw import PdfReader, PdfWriter, PdfDict
import json


class PdfFiller:

    output_pdf = ""
    pages = []
    data = {}

    # Initialize a PdfFiller object.
    def __init__(self, input_pdf, data_file):
        self.input_pdf = input_pdf
        self.pages = input_pdf.pages
        self.load_data(data_file)
        self.set_output(path = "resources/filled-sample.pdf")
        
    # Load data from json to dict.
    def load_data(self, data_in) -> None:
        with open(data_in, 'r') as json_file:
            self.data = json.load(json_file)

    # Set output path.
    def set_output(self, path) -> None:
        self.output_pdf = path

    # Get output path.
    def get_output(self) -> str:
        return str(self.output_pdf)
    
    # Form-filler procedure.
    def fill_forms(self) -> None:
        for annotation in self.pages[0]['/Annots']:
            if annotation['/T']:
                annotation.update(
                    PdfDict(
                    V='{}'.format(self.data[annotation['/T'][1:-1]]))
                )
        PdfWriter().write(self.output_pdf, self.input_pdf)


pdf_reader = PdfReader(sys.argv[1])
data_file = sys.argv[2]

fillerObject = PdfFiller(pdf_reader, data_file)
fillerObject.fill_forms()
print(fillerObject.get_output())
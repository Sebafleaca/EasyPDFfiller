import sys
from pdfrw import PdfReader, PdfWriter, PdfDict
import json


class PdfFiller:

    output_pdf = "resources/complex-filled.pdf"
    pages = []
    data = {}
    num_errors = 0
    errors = []

    # Initialize a PdfFiller object.
    def __init__(self, input_pdf, data_file):
        self.input_pdf = input_pdf
        self.pages = input_pdf.pages
        if len(self.pages) <= 0:
            self.add_error(self.num_errors, "PDF has no pages")
        self.load_data(data_file)

    # Load data from json to dict.
    def load_data(self, data_in) -> None:
        with open(data_in, 'r') as json_file:
            self.data = json.load(json_file)
        if not self.data:
            self.add_error("No data in the JSON")

    # Form-filler procedure.
    def fill_forms(self) -> str:
        '''
        PDF's form's keys.
        E.g.    annots[form_type] gives the type of the form
                annots[text_field] gives the name of the text field
        '''
        form_type = '/FT'
        text_field = '/Tx'
        button_field = '/Btn'
        field_name = '/T'

        '''
        'Ff' key's flags. Assign their sum to PdfDict(Ff).
        E.g.    annots.update(PdfDict(Ff=read_only+required))
        '''
        read_only = 2**0     # first bit (low-order) set to 1
        required = 2**1      # second bit (low-order) set to 1
        radio = 2**16        # 16th bit set to 1, otherwise is a checkbox

        for page in self.pages:
            if page:
                for annot in page['/Annots']:

                    if annot[form_type] == text_field:
                        flags = read_only+required
                        self.fill_text_fields(annot, field_name, flags=flags)

                    elif annot[form_type] == button_field:
                        self.manage_button_fields(annot, field_name)

                    else:
                        self.add_error("Unknown field type")
            else:
                self.add_error("PDF's page is empty")

        if len(self.errors) == 0:
            PdfWriter().write(self.output_pdf, self.input_pdf)
        else:
            print("Errors: ")
            index = 0
            for error in self.errors:
                print(index, ": " + self.errors[index])
                index += 1
            raise Exception("Errors encountered, writing not possible.")

        return str(self.output_pdf)

    # Put data in all text-field forms.
    def fill_text_fields(self, annotation, field_name, flags=0) -> None:
        max_length = 255

        if annotation[field_name]:
            # print(annot[field_name], "text")
            data_to_fill = self.data[annotation[field_name][1:-1]]
            if annotation['/MaxLen']:
                max_length = annotation['/MaxLen']
            if len(str(data_to_fill)) <= int(max_length):
                try:
                    annotation.update(PdfDict(
                        V='{}'.format(data_to_fill),
                        Ff=flags)
                    )
                except:
                    raise Exception(
                        "Can't instantiate 'PdfDict'.")
            else:
                self.add_error("Text field's MaxLen exceeded")
        else:
            self.add_error("Form's name is empty")

    # Set button-field forms.
    def manage_button_fields(self, annotation, field_name, flags=0) -> None:
        '''
        if annotation[field_name]:
            # print("Button", annotation[field_name][1:-1])
            annotation.update(
                PdfDict(Off=self.data[annotation[field_name][1:-1]]))
            # print(annotation['/Off'])
        else:
            # print("Button field has no name")
            # print(annotation['/Off'])
        '''

    # Push a new error to the errors array
    def add_error(self, new_error):
        self.errors.insert(self.num_errors, new_error)
        self.num_errors += 1


if len(sys.argv) != 3:
    raise Exception("Wrong number of arguments.\n"
                    + "Usage: python EasyPDFfiller.py "
                    + "pdf-file.pdf data-file.json")
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

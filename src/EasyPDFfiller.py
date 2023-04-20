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
            self.add_error("PDF has no pages")
        self.load_data(data_file)

    # Load data from json to dict.
    def load_data(self, data_in) -> None:
        try:
            with open(data_in, 'r') as json_file:
                self.data = json.load(json_file)
        except:
            self.add_error("Can't read JSON file")
        if not self.data:
            self.add_error("Can't read JSON file")

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
        Or simply modify the 'flags' variable:
        E.g.    flags=read_only+required
        '''
        read_only = 2**0     # first bit (low-order) set to 1
        required = 2**1      # second bit (low-order) set to 1
        radio = 2**16        # 16th bit set to 1, otherwise is a checkbox

        for page in self.pages:
            if page['/Annots']:
                for annot in page['/Annots']:
                    if not "Can't read JSON file" in self.errors:
                        if annot[form_type] == text_field:
                            flags = read_only
                            self.fill_text_fields(annot, field_name, flags)
                        elif annot[form_type] == button_field:
                            self.manage_button_fields(annot, field_name)
                        else:
                            self.add_error(str(annot[field_name])
                                           + " has unknown field type")
            else:
                self.add_error("PDF's page is empty")

        if len(self.errors) == 0:
            PdfWriter().write(self.output_pdf, self.input_pdf)
            return_string = str(self.output_pdf)
        else:
            print("Errors: ")
            index = 0
            for error in self.errors:
                print(str(index) + ": " + self.errors[index])
                index += 1
            return_string = ("Errors encountered, filling not possible.")

        return return_string

    # Put data in all text-field forms.
    def fill_text_fields(self, annotation, field_name, flags=0) -> None:
        max_length = 255

        if annotation[field_name]:
            data_to_fill = ""
            try:
                data_to_fill = self.data[annotation[field_name][1:-1]]
            except:
                self.add_error("Field name "
                               + str(annotation[field_name])
                               + " not in JSON data")
            if annotation['/MaxLen']:
                max_length = annotation['/MaxLen']
            if len(str(data_to_fill)) <= int(max_length):
                try:
                    annotation.update(PdfDict(
                        V='{}'.format(data_to_fill),
                        Ff=flags)
                    )
                except:
                    self.add_error("Can't update text form "
                                   + str(annotation[field_name]))
            else:
                self.add_error("Text field's MaxLen exceeded")
        else:
            self.add_error("Form's name is empty")

    # Set button-field forms.
    def manage_button_fields(self, annotation, field_name, flags=0) -> None:
        '''
        if annotation[field_name]:
            # print("Button", annotation[field_name][1:-1])
            try:
                annotation.update(
                    PdfDict(Off=self.data[annotation[field_name][1:-1]]))
            except:
                self.add_error("Can't update button form")
            # print(annotation['/Off'])
        else:
            # self.add_error("Button field has no name")
        '''

    # Push a new error to the errors array
    def add_error(self, new_error):
        self.errors.insert(self.num_errors, new_error)
        self.num_errors += 1


if len(sys.argv) != 3:
    raise ImportError("Wrong number of arguments."
                      + "\nUsage: python EasyPDFfiller.py "
                      + "pdf-file.pdf data-file.json")
if not sys.argv[1].endswith(".pdf"):
    raise ImportError("First argument must be a PDF file.")
if not sys.argv[2].endswith(".json"):
    raise ImportError("Second argument must be a JSON file.")

try:
    pdf_reader = PdfReader(sys.argv[1])
except:
    raise ImportError("Can't read PDF file.")
try:
    data_file = sys.argv[2]
except:
    raise ImportError("Can't read JSON file.")

fillerObject = PdfFiller(pdf_reader, data_file)
print(fillerObject.fill_forms())

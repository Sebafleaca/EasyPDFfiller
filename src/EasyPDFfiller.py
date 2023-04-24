import sys
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
import json


class PdfFiller:

    input_path = ""
    output_path = ""
    pdf_reader = PdfReader
    pages = []
    data = {}
    num_errors = 0
    errors = []
    num_warnings = 0
    warnings = []

    # Initialize a PdfFiller object.
    def __init__(self, input_pdf, data_file, output_pdf="") -> None:
        self.input_path = input_pdf
        if output_pdf != "":
            self.output_path = output_pdf
        else:
            self.output_path = self.input_path.replace(".pdf", "-filled.pdf")
        try:
            self.pdf_reader = PdfReader(input_pdf)
        except:
            raise AttributeError("Can't read PDF file")
        self.pages = self.pdf_reader.pages
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
            self.add_error("No data in the JSON file")

    # Form-filler procedure.
    def fill_forms(self, flatten=True) -> str:
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
        radio = 2**16        # 16th bit set to 1, if not it's a checkbox

        for page in self.pages:
            if page['/Annots']:
                for annot in page['/Annots']:
                    if not "Can't read JSON file" in self.errors:
                        if annot[form_type] == text_field:
                            flags = read_only
                            self.fill_text_field(
                                annot, field_name, flatten, flags
                            )
                        elif annot[form_type] == button_field:
                            self.manage_button_field(
                                annot, field_name, flatten
                            )
                        else:
                            self.add_warning(str(annot[field_name])
                                             + " has unknown field type")
            else:
                self.add_error("PDF's page is empty")

        if len(self.errors) == 0:
            PdfWriter().write(self.output_path, self.pdf_reader)
            return_string = str(self.output_path)
        else:
            print("Errors: ")
            index = 0
            for error in self.errors:
                print(str(index) + ": " + self.errors[index])
                index += 1
            return_string = ("Errors encountered, filling not possible.")

        return return_string

    # Put data in a text-field form.
    def fill_text_field(self, annotation, field_name, flatten, flags=0) -> None:
        max_length = 255

        if annotation[field_name]:
            if annotation['/MaxLen']:
                max_length = annotation['/MaxLen']
            key = annotation[field_name][1:-1]
            if key in self.data.keys():
                data_to_fill = self.data[key]
                if len(str(data_to_fill)) <= int(max_length):
                    try:
                        annotation.update(
                            PdfDict(V='{}'.format(data_to_fill))
                        )
                    except:
                        self.add_error("Can't update text form "
                                       + str(annotation[field_name]))
                    try:
                        if flatten:
                            value = self.flatten_form(annotation['/Ff'])
                            annotation.update(PdfDict(Ff=value))
                    except:
                        self.add_error("Can't flatten text form "
                                       + str(annotation[field_name]))
                else:
                    self.add_error("Text field's MaxLen exceeded")
            else:
                self.add_warning("Form '"
                                 + str(annotation[field_name])
                                 + "' not found in JSON")
        else:
            self.add_warning("Form '"
                             + str(annotation[field_name])
                             + "' not found in JSON")

    # Set button-field form.
    def manage_button_field(self, annotation, field_name, flatten, flags=0) -> None:

        if annotation[field_name]:
            key = annotation[field_name][1:-1]
            if key in self.data.keys():
                try:
                    if type(self.data[key]) == bool:
                        if self.data[key] == True:
                            annotation.update(PdfDict(AS=PdfName('Yes')))
                        elif self.data[key] == False:
                            annotation.update(PdfDict(AS=PdfName('Off')))
                        else:
                            self.add_warning("Unknown value for form '"
                                             + annotation[field_name]
                                             + "'")
                    else:
                        if self.data[key] == "Yes":
                            annotation.update(
                                PdfDict(V='Yes', AS=PdfName('Yes'))
                            )
                        elif self.data[key] == "No":
                            annotation.update(
                                PdfDict(V='{}'.format(self.data[key]),
                                        AS=PdfName('Off'))
                            )
                        else:
                            self.add_warning("Unknown value for form '"
                                             + annotation[field_name]
                                             + "'")
                except:
                    self.add_error("Can't update form '"
                                   + annotation[field_name]
                                   + "'")
                try:
                    if flatten:
                        value = self.flatten_form(annotation['/Ff'])
                        annotation.update(PdfDict(Ff=value))
                except:
                    self.add_error("Can't flatten button form "
                                   + str(annotation[field_name]))
        else:
            self.add_warning("Form '"
                             + str(annotation[field_name])
                             + "' not found in JSON")

    # Flatten (i.e. make read-only) a form.
    def flatten_form(self, flag_value) -> int:
        ff = 0
        if flag_value == None:
            ff = 1
        else:
            str_flag_value = str(flag_value)
            int_flag_value = int(str_flag_value)
            if int_flag_value % 2 == 0:
                ff = int_flag_value + 1
        return ff

    # Push a new error to the errors array.
    def add_error(self, new_error) -> None:
        self.errors.insert(self.num_errors, new_error)
        self.num_errors += 1

    # Push a new warning to the warnings array.
    def add_warning(self, new_warning) -> None:
        self.warnings.insert(self.num_warnings, new_warning)
        self.num_warnings += 1


if len(sys.argv) < 3:
    raise ImportError("Wrong number of arguments."
                      + "\nUsage: python EasyPDFfiller.py "
                      + "[input-pdf].pdf [data-file].json"
                      + "(optional: [output-pdf].pdf)")
if not sys.argv[1].endswith(".pdf"):
    raise ImportError("First argument must be a PDF file.")
if not sys.argv[2].endswith(".json"):
    raise ImportError("Second argument must be a JSON file.")

if len(sys.argv) == 4:
    filler = PdfFiller(sys.argv[1], sys.argv[2], sys.argv[3])
elif len(sys.argv) == 3:
    filler = PdfFiller(sys.argv[1], sys.argv[2])
print(filler.fill_forms())

import sys
from pdfrw import PdfReader, PdfWriter, PdfDict
import json

# Load data from json to dict
with open('sample-data.json', 'r') as data_file:
    data = json.load(data_file)

# In/Out paths
input_pdf = PdfReader(sys.argv[1])
output_pdf = "filled-sample.pdf"

# Input file's pages
pages = input_pdf.pages

# Forms filler procedure
for annot in pages[0]['/Annots']:
    if annot['/T']:
        annot.update(
            PdfDict(
            V='{}'.format(data[annot['/T'][1:-1]]))
        )

# Output filled file
PdfWriter().write(output_pdf, input_pdf)
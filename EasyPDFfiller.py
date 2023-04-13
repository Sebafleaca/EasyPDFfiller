import sys
from pdfrw import PdfReader, PdfWriter, PdfDict

# In/Out paths
input_pdf = PdfReader(sys.argv[1])
output_pdf = "filled-sample.pdf"

# Input file's pages
pages = input_pdf.pages

# Dict with sample values to fill in forms
data = {
    'NameKey': 'Bugs',
    'SurnameKey': 'Bunny',
    'AgeKey': 84
}

# Forms filler procedure
for annot in pages[0]['/Annots']:
    if annot['/T']:
        annot.update(
            PdfDict(
            V='{}'.format(data[annot['/T'][1:-1]]))
        )

# Output filled file
PdfWriter().write(output_pdf, input_pdf)
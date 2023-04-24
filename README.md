# EasyPDFfiller  
**powered by pdfrw**

### Script usage:
run: `$ python src/EasyPDFfiller.py [fillable-pdf].pdf [data-file].json (optional: [filled-pdf].pdf)`

**Example:**  
try: `$ python src/EasyPDFfiller.py resources/inputPDF.pdf resources/input-data.json resources/filled-document.pdf`


### Unit test usage:
run: `$ python src/test.py [fillable-pdf-name].pdf [data-file-name].json`

**Example:**  
run: `$ python src/test.py resources/sample-input.pdf resources/sample-data.json`

### Developer's guide:
The constructor for 'PdfFiller' gets two (or three) params as command line arguments:
- the path for the fillable pdf to edit;
- the path for the json containing the data to fill in;
- optional: the path for the output pdf.

**Example:**  
`import sys`  
`filler = PdfFiller(sys.argv[1], sys.argv[2])`

`$ python src/EasyPDFfiller.py fillable-pdf.pdf fill-in-data.json`

Then call the method 'fill_forms()' to fill the data in the pdf and get the path for the filled pdf.

**Example:**  
`filler.fill_forms()`
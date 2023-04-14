# EasyPDFfiller  
**powered by pdfrw**

### Script usage:
run: `$ python src/EasyPDFfiller.py [fillable-pdf-name].pdf [data-file-name].json`

**Example:**  
run: `$ python src/EasyPDFfiller.py resources/sample-input.pdf resources/sample-data.json`


### Unit test usage:
run: `$ python src/test.py [fillable-pdf-name].pdf [data-file-name].json`

**Example:**  
run: `$ python src/test.py resources/sample-input.pdf resources/sample-data.json`

### Developer's guide:
The constructor for 'PdfFiller' gets two params as command line arguments:
- the fillable pdf to edit;
- the json containing the data to fill in.

**Example:**  
`import sys`  
`fillerObject = PdfFiller(sys.argv[1], sys.argv[2])`

`$ python src/EasyPDFfiller.py fillable-pdf.pdf fill-in-data.json`

Then call the method 'fill_forms()' to fill the data in the pdf.

**Example:**  
`fillerObject.fill_forms()`

Finally, in order to get the path for the filled pdf, call the method 'get_output'.

**Example:**  
`fillerObject.get_output()`
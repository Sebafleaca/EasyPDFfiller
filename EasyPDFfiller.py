import sys
import PyPDF2


read_PDF = PyPDF2.PdfReader(sys.argv[1])
pages = read_PDF.pages
num_pages = read_PDF._get_num_pages()

# Split all the text in pages
text = []
index=0
for page in pages:
    text.insert(index, page.extract_text())
    index=index+1

# Retrieve text of all pages
index=0
for page in pages:
    print("Retrieving page number " + str(index) + ": ")
    print(text[index])
    index=index+1

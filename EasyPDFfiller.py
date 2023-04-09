import sys
import PyPDF2


read_PDF = PyPDF2.PdfReader(sys.argv[1])
pages = read_PDF.pages
num_pages = read_PDF._get_num_pages()

# Split all the text in pages
text = []
xform_text = []
index=0
for page in pages:
    
    ''' What can be retrieved from a PDF page?'''

    # This only prints "/Filter"
    for content in page.get_contents():
        print(content)
    # This prints "{'/Filter: '/FlateDecode'}"
    print(page.get_contents())
    # This prints contents in XML format
    print(page.get_contents)
    # This prints all text in XML format
    print(page.extract_xform_text)
    # This prints all text in plain text
    print(page.extract_text)

    # Doesn't work
    # for content in page.get_contents():
    #    print(page.extract_xform_text(content))

    xform_text.insert(index, page.extract_xform_text)
    text.insert(index, page.extract_text)
    index=index+1

# Retrieve text of all pages
index=0
for page in pages:
    print("\nRetrieving page number " + str(index) + ": ")
    print(text[index])
    index=index+1

import PyPDF2
import urllib
import os.path



def split_pdf_into_pages(pdf_filepath, pdf_outpaths="./download/splitted_pdf_%s.pdf", password=None):
    inputpdf = PyPDF2.PdfFileReader(open(pdf_filepath, "rb"))
    if inputpdf.isEncrypted:
        if password == None:
            print "Encrypted PDF and no password given."
            return False
        inputpdf.decrypt(password)
    texts = []
    for i in xrange(inputpdf.numPages):
        outputpdf = PyPDF2.PdfFileWriter()
        cur_page = inputpdf.getPage(i)
        texts.append(cur_page.extractText())
        outputpdf.addPage(cur_page)
        with open(pdf_outpaths % i, "wb") as outputStream:
            outputpdf.write(outputStream)
    return texts

def download_pdf(url):
    f = urllib.URLopener()
    fname = "./download/downloaded_pdf_%s"
    i=1
    while(os.path.isfile("./"+(fname % i)+".pdf")):
        i=i+1
    f.retrieve(url, "./"+(fname % i)+".pdf")
    return "./"+(fname % i)+".pdf"


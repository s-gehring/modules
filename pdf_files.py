from pyPDF2
import urllib
import os.path



def split_pdf_into_pages(pdf_filepath, pdf_outpaths, password=None):
  inputpdf = PdfFileReader(open(pdf_filepath, "rb"))
  if inputpdf.isEncrypted:
    if password == None:
      #aklsadjf
    #asdklfja
  for i in xrange(inputpdf.numPages):
    outputpdf = PdfFileWriter()
    cur_page = inputpdf.getPage(i)
    cur_text = cur_page.extractText()
    outputpdf.addPage(cur_page)
    with open(pdf_outpaths % i, "wb") as outputStream:
      outputpdf.write(outputStream)
      
def download_pdf(url):
  f = urllib.URLopener()
  fname = "downloaded_pdf_%s"
  i=1
  while(os.path.isfile("./"+(fname % i)+".pdf")):
    i=i+1
  f.retrieve(url, "./"+(fname % i)+".pdf")
  return "./"+(fname % i)+".pdf"
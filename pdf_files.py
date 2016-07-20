import PyPDF2
import urllib
import os.path

texts = []

def get_pdf_pages(small_id):
    small_id = small_id.replace(u" ","")
    global texts
    pages = []
    for i in range(len(texts)):
      if small_id in texts[i]:
        pages.append(i)
    return pages

def handle_handbook(link, name, remove_tempfile = False):
  print "Downloading PDF [%s]..." % name,
  dl_pdf, success = download_pdf(link, name)
  print "done!"
  
  print "Processing PDF [%s]..." % name,
  splitted_texts = split_pdf_into_pages(dl_pdf, "./download/master_pdf_%s.pdf", write_to_file= success)
  print "done!"

  if remove_tempfile:
    os.remove(dl_pdf)
  texts.extend(splitted_texts)


def split_pdf_into_pages(pdf_filepath, pdf_outpaths="./download/splitted_pdf_%s.pdf", password=None, write_to_file=True):
    inputpdf = PyPDF2.PdfFileReader(open(pdf_filepath, "rb"))
    if inputpdf.isEncrypted:
        if password == None:
            print "Encrypted PDF and no password given."
            return False
        inputpdf.decrypt(password)
    texts = []
    for i in xrange(inputpdf.numPages):
        cur_page = inputpdf.getPage(i)
        texts.append(cur_page.extractText())
        if write_to_file:
	  outputpdf = PyPDF2.PdfFileWriter()
	  outputpdf.addPage(cur_page)
	  with open(pdf_outpaths % str(i).zfill(3), "wb") as outputStream:
	      outputpdf.write(outputStream)
    return texts

def download_pdf(url, fname="download"):
    f = urllib.URLopener()
    fullname = './download/'+fname+'.pdf'
    if os.path.isfile(fullname):
        return fullname, False
    filename, headers = f.retrieve(url, fullname)
    print headers
    return fullname, True


from tidylib import tidy_document
from bs4 import BeautifulSoup as bs
import urllib2


def get_url_text(url):
    return urllib2.urlopen(url).read()

def get_url_tidy_text(url):
    x = tidy_document(get_url_text(url), options={
      "indent":0,
      "tidy-mark":0,
      "wrap":0,
      "char-encoding":"raw",
      "doctype":"transitional",
      "preserve-entities":True,
      "quiet":True,
      "tidy-mark":False
    })[0]

    return x

def get_url_data(url):
    return bs(get_url_tidy_text(url), "html.parser")

def get_content(url):
    return get_url_data(url).find(class_="divcontent")

def get_all_tables(url):
    # Tidy_document places everything into a hr.
    # This is not in the slightest allowed, but at least it's
    # consistent, so I won't complain.
    get_content(url).find(class_=u'content')
    c = get_content(url)
    if c.div.hr == None:
        return True,
    return False,

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:52:57 2016

@author: simon
"""
#%%
import zlib
import urllib2
import string
import json
import pdf_files as pdf
import time
import os
from tidylib import tidy_document

import tree
import io


links = {
  'basis': {
	'all' : 'https://basis.uni-bonn.de/qisserver/rds;?state=wtree&search=1&category=veranstaltung.browse&navigationPosition=lectures%2Clectureindex&breadcrumb=lectureindex&topitem=lectures&subitem=lectureindex&noDBAction=y&init=y',
	'cs'  : 'https://basis.uni-bonn.de/qisserver/rds;jsessionid=627B1CCB1D9C3F205EE047E7D1FB66F0?state=wtree&search=1&trex=step&root120161=130415|140415&P.vx=lang',
	'csm' : 'https://basis.uni-bonn.de/qisserver/rds?state=wtree&search=1&trex=step&root120161=130415|140415|140430&P.vx=lang'
      },
  'modules':{
	'BSc' : 'https://www.informatik.uni-bonn.de/de/dateien/master_cs/Modulhandbuch-BSc-Informatik.pdf',
	'MSc' : 'https://www.informatik.uni-bonn.de/en/files/master_cs/Modulhandbuch-MSc-CS-4.pdf'
      }
  }


pdf.handle_handbook(links['modules']['MSc'], "Master")
pdf.handle_handbook(links['modules']['BSc'], "Bachelor")


url = links['basis']['cs']

start = time.time()
s = tree.get_tree(url, deep_search=False) # Deep-Search: Look for dedicated pages instead of just tables for lectures.
end = time.time()

if not os.path.exists('./output/'):
  os.makedirs('./output/')

with open("./output/modulhandbuch.zlib.json", 'w+') as f:
    f.write(zlib.compress(json.dumps(s)))
with open("./output/modulhandbuch.json", 'w+') as f:
    f.write(json.dumps(s))
with open("./output/notes.txt", 'w+') as f:
    f.write("Link to analyze: '"+url+"'\n")
    f.write("Time needed: "+io.seconds_to_time(end-start)+ "\n")
    f.write("Global Nodes: "+str(tree.global_nodes)+"\n")
    f.write("Global Leaves:"+str(tree.global_leaves)+"\n")
    f.write("Global Lectures:"+str(tree.global_lectures)+"\n")
print "Found",tree.global_nodes,"folders with",tree.global_leaves,"files in total with",tree.global_lectures,"lectures in total."
#print(zlib.compress(json.dumps(s)))


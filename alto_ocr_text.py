#!/usr/bin/env python
# Usage: python alto_ocr_text.py <altofile>

import codecs
import os
import sys
import xml.etree.ElementTree as ET



if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
             'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
             'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
             'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#' }

altodir = sys.argv[1]
outdir = sys.argv[2]

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(altodir) if isfile(join(altodir, f))]

print(onlyfiles)


def writeToFile (filename, content):

   outFile=open(filename, "w")
   outFile.write(content)
   outFile.close()



for file in onlyfiles:

    outfile = altodir + "/" + file

    tree = ET.parse(outfile)
    
    outfile = outdir + "/" + file.replace(".xml",".txt")

    print(outfile)


    xmlns = tree.getroot().tag.split('}')[0].strip('{')
    if xmlns in namespace.values():
        for lines in tree.iterfind('.//{%s}TextLine' % xmlns):
            sys.stdout.write('\n')
            for line in lines.findall('{%s}String' % xmlns):
               text = line.attrib.get('CONTENT') + ' '
               sys.stdout.write(text)
               writeToFile(outfile, text)
    else:
        print('ERROR: Not a valid ALTO file (namespace declaration missing)')


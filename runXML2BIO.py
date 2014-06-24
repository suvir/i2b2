'''
Created on May 19, 2014

@author: shitij
'''
import os
from newXML2BIO import xml2bio

DIRPATH = "/home/shitij/i2b2/data/training-RiskFactors-Gold-Set2/"
fileList = os.listdir(DIRPATH)

for index,fn in enumerate(fileList):
    if fn.endswith(".xml"):
        print "Running on: ",fn
        xml2bio(DIRPATH+"/"+fn)
        print "Done: ",fn," (",index+1," / ",len(fileList)," )\n"

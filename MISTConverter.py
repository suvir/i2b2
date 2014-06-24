'''
Created on May 25, 2014

@author: shitij
'''

##NOTE: If you want to use this script, please note that file source/destination(s) are hardcoded in it
## You will need to change them (Like input directory and output directory)

from lxml import etree
import os
import nltk
import collections

#path of the directory where the xmls are
XML_DIR_PATH = "/home/shitij/i2b2/data/training-PHI-Gold-Set1/"

#build a dictionary of all the tags in the gold standard
def buildTagDictionary(xml):
    
    elementList = xml.findall(".//*[@start]") #get all tags with start attribute
    
    tagDictionary = collections.OrderedDict()
    for element in elementList:
        elementText=element.get("text")
        elementStart=int(element.get("start"))
        elementEnd = int(element.get("end"))
        elementTag = element.tag
        elementType = element.get("TYPE")
        
        tagDictionary[(elementStart,elementEnd)]=(elementText,elementTag,elementType)
         
    return tagDictionary

def convertToMist(xmlPath):
    
    #parse XML file
    tree=etree.parse(xmlPath)
    xml = tree.getroot()

    #get the text part in XML
    for tags in xml.iter('TEXT'):
        text=tags.text
    
    tagDictionary = buildTagDictionary(xml)
    
    root = etree.Element("__top")
    zoneElement = etree.SubElement(root, "zone")
    zoneElement.set("region_type","body")
    
    #tokenize the text
    end=0
    for key in tagDictionary:
        start,endTemp = key
        
        #tokenize the text between tags
        textBetweenTagsList = nltk.word_tokenize(text[end:start])

        if len(textBetweenTagsList)!=0:
            for token in textBetweenTagsList:
                lexElement = etree.SubElement(zoneElement, "lex")
                lexElement.text = token
          
        end=endTemp 
          
        #now we have the tag text
        tokenText, elementTag, elementType = tagDictionary[key]

        tagTextTokens = nltk.word_tokenize(tokenText)
        if len(tagTextTokens)==1:
            lexElement = etree.SubElement(zoneElement, "lex")
            tagElement = etree.SubElement(lexElement,elementTag)
            tagElement.text = tokenText
            tagElement.set("TYPE",elementType)
        else:
            tagElement = etree.SubElement(zoneElement,elementTag)
            tagElement.set("TYPE",elementType)
            for tagToken in tagTextTokens:
                lexElement = etree.SubElement(tagElement, "lex")
                lexElement.text = tagToken
    
    fileName = xmlPath.split("/")
    fileName = fileName[len(fileName)-1].replace(".xml",".mistphi.xml")
    filePath = "/home/shitij/i2b2/data/mistXML/"+fileName
    phiFile = open(filePath,"w")
    print filePath
    phiFile.write(etree.tostring(root, pretty_print=True))
    #print(etree.tostring(root, pretty_print=True))
    phiFile.close()
    
def main():
    fileList = os.listdir(XML_DIR_PATH)
    for index,fileName in enumerate(fileList):
        convertToMist(XML_DIR_PATH+fileName)
        print "Done:",fileName,"( ",index+1," / ",len(fileList)," )"
    
main()
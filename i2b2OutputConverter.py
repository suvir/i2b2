## NOTE: If you need to use this script, you must change the hardcoded file source/ destinations paths
## in the main() function at the bottom of this script file

import re
from lxml import etree
import os


def originalTextSentences(origFile):
    fileSent = open(origFile,"r")
    allText = fileSent.read()
    textSentenceList = allText.split("\n")#re.compile(r'(\n)').split(allText)#allText.split("\n")
    for index,thing in enumerate(textSentenceList):
        print index+1, " : ",thing
    return textSentenceList

#get the tag list from the .i2b2.entries file        
def getMedTagList(tagMedFile):
    medTagList = []
    fileMedTag = open(tagMedFile, "r")
    medText = fileMedTag.read()
    medTextSentences = medText.split("\n")
    for sentence in medTextSentences:
        #the fields are separated by ||
        token = sentence.split("||")[0]
        if token.strip()!="":
            matchObj = re.search(r'^m="(.+)" (\d*):(\d*) (\d*):(\d*)',token)
            textTokens = matchObj.group(1).split()#have to do because of bug in medication program
            #a:b c:d, d is not correct sometimes (bug in medication program), so count text tokens and calculate yourself
            startSent = int(matchObj.group(2))
            startToken = int(matchObj.group(3))
            endSent = int(matchObj.group(4))
            if startSent == endSent:
                endTokenOffset = int(matchObj.group(3))
            else:
                endTokenOffset = -1
                    
            endToken =  endTokenOffset+ len(textTokens) - 1
            
            medTagList.append((matchObj.group(1),startSent,startToken,endSent,
                              endToken))
    return medTagList

#given a sentence number and the token number inside that sentence
#return the start and end character indices of the token
def getTokenStartEndChar(textSentenceList,sentNum,tokNum):
    
    #start char of startTok
    charCount=0
    for index,sentence in enumerate(textSentenceList):
        if index+1==sentNum:#the sentence before
            break
        charCount += len(sentence)
        
    #You have the count till the sentence before, now get the count in current sentence
    tokIndex=-1
    for token in re.compile(r'(\s+)').split(sentence):#split, keeping whitespaces  
        lastCharCount = charCount     
        charCount += len(token)
        if token.strip()!="":#dont count whitespaces as tokens
            tokIndex += 1
        if tokIndex == tokNum:
            start = lastCharCount
            end = charCount
            break
        
    #print (start,end-1)
    return (start,end-1)

def getCharBoundaries(textSentenceList,startSent,startTok,endSent,endTok):
    
    startStartTok, _ = getTokenStartEndChar(textSentenceList, startSent, startTok)
    _, endEndTok = getTokenStartEndChar(textSentenceList, endSent, endTok)
    return (startStartTok, endEndTok)
    
    
def convertToOutputFormat(origFile, tagMedFile):    
    #get the sentences from the original file
    textSentenceList = originalTextSentences(origFile)
    medTagList = getMedTagList(tagMedFile)
    
    root = etree.Element("TAGS")
    for tag in medTagList:
        text, startSent,startTok,endSent,endTok = tag
        start, end = getCharBoundaries(textSentenceList,startSent,startTok,endSent,endTok)
        medElement = etree.SubElement(root,"MEDICATION")
        medElement.set("start",str(start))
        medElement.set("end",str(end))
        medElement.set("text",text)
        medElement.set("indicator","")
        medElement.set("time","")
        medElement.set("comment","")

    return root

def convertFile(origFile,tagMedFile,outputPath):
    #origFile = "/home/shitij/abc.orig"
    #tagMedFile = "/home/shitij/abc.tag"
#    origFile = "/home/shitij/i2b2/umlsData/2014orig/220-01.orig"
#   tagMedFile = "/home/shitij/i2b2/umlsData/2014tag-med/220-01.i2b2.entries"
    
#   dtdFile = "/home/shitij/i2b2/data/Track2-RiskFactors/cardiacRisk_distribution.dtd"
    rootXML = convertToOutputFormat(origFile, tagMedFile)
    #print etree.tostring(rootXML,pretty_print=True)
    
    #dtd = etree.DTD(open(dtdFile,"rb"))
    #if not dtd.validate(rootXML):
    #   print "Produced XML does not conform with the DTD: ",dtdFile
    #else:
    fileName = origFile.split("/")
    fileName = fileName[len(fileName)-1].replace(".orig",".output.xml")
    outputFile = open(outputPath+fileName,"w")
    outputFile.write(etree.tostring(rootXML,pretty_print=True))
    
def main():
    origDirPath = "/home/shitij/i2b2/umlsData/2014orig/"
    tagMedPath = "/home/shitij/i2b2/umlsData/2014tag-med/"
    outputPath = "/home/shitij/i2b2/umlsData/2014-i2b2output-med/"
    
    tagMedFiles = os.listdir(tagMedPath)
    
    #convertFile("/home/shitij/i2b2/umlsData/2014orig/358-02.orig","/home/shitij/i2b2/umlsData/2014tag-med/358-02.i2b2.entries","/home/shitij/")
    for index,fileName in enumerate(tagMedFiles):
        print "Converting:",fileName,"(",index+1,"/",len(tagMedFiles),")"
        origFile = fileName.replace(".i2b2.entries",".orig")
        convertFile(origDirPath+origFile,tagMedPath+fileName,outputPath)

main()
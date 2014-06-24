'''
Created on Jun 21, 2014

@author: shitij
'''
## To run the script on more than one file (batch of XMLs), see runXML2BIO.py instead
## For running it on a single file, you must hardcode the file path in the end of this script 

import re
from nltk.tokenize import sent_tokenize
from lxml import etree
import collections
from operator import itemgetter

#if the ranges overlap, merge them and return true, else return false
#assume the list is sorted
def rangesOverlap(tagList, currentIndex, nextIndex):
    currentStart, currentEnd, tagInfoString = tagList[currentIndex]
    nextStart,nextEnd, _ = tagList[nextIndex]
    
    #overlapping condition
    if nextStart>=currentStart and nextStart<currentEnd and nextEnd>=currentEnd:
        #delete nextElement
        del tagList[nextIndex]
        tagList[currentIndex] = (currentStart,nextEnd,tagInfoString)
        return True;
    else:
        return False
    
def buildTagDictionary(xml,text):
    elementList = xml.findall(".//*[@start]") #get all tags with start attribute 
    attributesToAdd = ["TYPE","type1","type2","indicator","status","comment"]
    tagList = []
    for element in elementList:
        elementText=element.get("text")
        elementStart=int(element.get("start"))
        elementEnd = int(element.get("end"))
        elementTag = element.tag
        #the BIO string for the token
        tagInfoString="|"+elementTag+"|"+"start="+str(elementStart)+"|end="+str(elementEnd)+"|"
        
        for attribute in attributesToAdd:
            if element.get(attribute) is not None and element.get(attribute).strip()!="":
                tagInfoString+=attribute+"="+element.get(attribute)+"|"
                
        #manually trim and adjust spaces from beginning
        #To handle strings like " He does not smoke." (Note the leading space)
        for char in elementText:
            if not char.isspace():
                break
            else:
                elementStart += 1
                
        #manually trim and adjust spaces from end
        for char in reversed(elementText):
            if not char.isspace():
                break
            else:
                elementEnd -= 1
                
        tagList.append((elementStart,elementEnd, tagInfoString))
    
    #sort wrt start, end
    tagList = sorted(tagList,key=itemgetter(0,1))

    #merge overlapping ranges
    currentIndex = 0
    nextIndex = 1
    while len(tagList)>1:
        if currentIndex == len(tagList)-1:
            break
        if not rangesOverlap(tagList, currentIndex, nextIndex):#check and merge ranges
            currentIndex+=1
            nextIndex+=1
    
    #now build the tag dictionary
    tagDictionary = collections.OrderedDict()
    for tag in tagList:
        startChar,endChar,tagInfoString = tag
        tagText = text[startChar:endChar]
        
        start=0
        end=0
        actualIndex=-1
        for token in re.compile(r'(\w+)').split(tagText):#tokenize on non-alphanumeric characters
            if token.strip()== "":
                end=start+len(token)
                start=end
                continue;
            else:
                actualIndex += 1
            BIOTag="I" 
            if actualIndex==0: #first token, means B
                BIOTag="B"
            end=start+len(token)
            if token.strip()!="":  #don't add spaces only tokens
                tagDictionary[(start+startChar,end+startChar,token)]=BIOTag+tagInfoString
            start=end
        
    return tagDictionary
    

#fix the sentence tokenized version to re-patch whitespaces
def patchWhitespacesInSentenceList(text,textSentences):        
    itext=0
    newSentenceList=[]
    for sentence in textSentences:
        newSentence=""
        iSent=0
        while iSent<len(sentence) and itext<len(text):
            #if not same
            if text[itext]!=sentence[iSent]:
                newSentence+=text[itext]
                itext+=1
            else:
                #they are same
                newSentence+=text[itext]
                itext+=1
                iSent+=1
        newSentenceList.append(newSentence)
        
    return newSentenceList    

def buildTokenDictionary(textSentences,tagDictionary):
    
    start=0
    end=0

    #take ordered dictionary, need to remember the insert order as we'll output this as it is later
    fullTextDict=collections.OrderedDict()
    
    #iterate over sentences
    for sentence in textSentences:
        tokens = re.compile(r'(\w+)').split(sentence)# split tokens, keeping whitespaces and sp chars 
    
        #iterate over tokens in each sentence
        for token in tokens:
            end+=len(token)
            flag=0
            if token.strip()=="":
                start=end
                continue

            if (start,end,token) in tagDictionary:
                fullTextDict[(start,end,token)]=tagDictionary[(start,end,token)]
                flag=1
    
            if flag==0: #ignore whitespaces, except newlines
                fullTextDict[(start,end,token)]='O'
                
            start=end
        #sentence end, insert newline
        fullTextDict[(end,end,"\n")]='O'
            
    return fullTextDict




#output the token Dictionary to file
def outputToFile(tokenDictionary, XMLFilePath):
    
    #output to same directory
    newFilePath = XMLFilePath.replace(".xml",".bio")
    
    f=open(newFilePath,"w")
    tokens = XMLFilePath.split("/")
    f.write(tokens[len(tokens)-1].replace(".xml",""))
    f.write("\n")
    for key in tokenDictionary:
        start, end, text = key
        value = tokenDictionary[key]
        if start==end:
            f.write("\n")
        else:
            mystring = text+"\t"+value+"\n"
            mystring2 =  mystring.encode('utf-8','ignore')
            f.write(mystring2)
    f.close()
    
    
    
    
def xml2bio(xmlPath):
    
    #parse XML file
    tree=etree.parse(xmlPath)
    xml = tree.getroot()

    text=""
    
    #get the text part in XML
    for tags in xml.iter('TEXT'):
        text=tags.text
        
    #You have the sentences in the text (does not preserve whitespaces fully)
    textSentences = sent_tokenize(text)
    
    #patch whitespaces
    textSentences=patchWhitespacesInSentenceList(text,textSentences)
    
    #read the tag part of the XML into dictionary
    tagDictionary=buildTagDictionary(xml,text)
    
    #build a dictionary of tokens from the original text
    tokenDictionary=buildTokenDictionary(textSentences,tagDictionary) 
    
    outputToFile(tokenDictionary, xmlPath)       

xml2bio("/home/shitij/i2b2/data/training-RiskFactors-Complete-Set2/100-01.xml")
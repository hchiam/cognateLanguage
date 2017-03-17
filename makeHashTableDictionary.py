from dictAsFile_wrapper import *


def getDict_fromTxt(dictFileName):
    d = {}
    with open(dictFileName) as f:
        for line in f:
           splitLine = line.replace('\n','').split(',')
           key = splitLine[1]
           val = splitLine[0]
           d[key] = val
    return d

def createHashTable_fromTxt():
    txtFileName = 'output_shortlist.txt'
    d = getDict_fromTxt(txtFileName)
    outputHTName = 'hashtable.pkl'
    writeDictToFile(d,outputHTName)


# this if statement is so that the following code only runs if this .py file is not being imported
if __name__ == '__main__':
    createHashTable_fromTxt()
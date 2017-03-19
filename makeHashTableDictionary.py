from dictAsFile_wrapper import *


def txt_to_dict(txtFileName):
    d = {}
    with open(txtFileName) as f:
        for line in f:
           splitLine = line.replace('\n','').split(',')
           key = splitLine[1]
           val = splitLine[0]
           d[key] = val
    return d

def txt_to_HT():
    txtFileName = 'output_shortlist.txt'
    d = txt_to_dict(txtFileName)
    outputHTName = 'hashtable.pkl'
    writeDictToFile(d,outputHTName)


# this if statement is so that the following code only runs if this .py file is not being imported
if __name__ == '__main__':
    txt_to_HT()
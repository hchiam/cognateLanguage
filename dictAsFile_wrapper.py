# basic wrapper around python pickle to use a dictionary as a file

# to import this file and use its methods, copy this this following line: 
from dictAsFile_wrapper import * # copy this line to import its methods


import pickle


def writeDictToFile(d,fileName): # write dictionary to file
    outputFile = open(fileName, 'wb')
    pickle.dump(d, outputFile)
    outputFile.close()

def readFileToDict(fileName): # read file to dictionary
    pkl_file = open(fileName, 'rb')
    d = pickle.load(pkl_file)
    pkl_file.close()
    return d


# this if statement is so that the following code only runs if this .py file is not being imported
if __name__ == '__main__':
    # example use:
    myDict = {'a':1,'b':2,'c':3,'d':5}
    fileName = 'myfile.pkl'
    writeDictToFile(myDict,fileName)
    dictBack = readFileToDict(fileName)
    print myDict
    print dictBack
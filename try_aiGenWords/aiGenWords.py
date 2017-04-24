from evalWord import *
from random import randint

inputFile = 'data.txt'
data = []
outputFile = 'output.txt'

def getData():
    with open(inputFile,'r') as f:
        data = f.readlines()
    return data

def getError(word):
    return round(evaluateLine(word)[2], 2)

def generateWord(entry):
    outputWord = ''
    entry = entry.split(',')
    srcWords = entry[2:7]
    print(srcWords)
    # track letters left in each source word
    letters = [0,0,0,0,0]
    for i in range(5):
        letters[i] = len(srcWords[i])
    print(letters)
    # track current focus
    lang = 0 # 'c' 's' 'h' 'a' 'r'
    while (all(letters[i] > 0 for i in range(len(letters)))):
        outputWord += srcWords[lang]
        letters[lang] -= 1
        lang = randint(0,9)
    return outputWord

data = getData()
for i in range(len(data)):
    print(generateWord(data[i]))
for i in range(len(data)):
    print(getError(data[i]))
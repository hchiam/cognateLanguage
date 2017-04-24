from evalWord import *
from random import randint

inputFile = 'data.txt'
data = []
outputFile = 'output.txt'
newWords = []
output = []



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
    print(entry[1] + " : " + str(srcWords))
    # track letters left in each source word
    letters = [0,0,0,0,0]
    for i in range(5):
        letters[i] = len(srcWords[i])-1
    # track current focus
    lang = 0 # 0=c, 1=s, 2=h, 3=a, 4=r
    # randomly get letters from source words
    while (all(letters[i] > 0 for i in range(len(letters)))):
        letterToAdd = srcWords[lang][len(srcWords[lang])-letters[lang]-1]
        outputWord += letterToAdd
        letters[lang] -= 1
        lang = randint(0,4)
    return outputWord



data = getData()

for i in range(len(data)):
    newWord = generateWord(data[i])
    newWords.append(newWord)
    output.append(newWord + ',' + data[i].split(',',1)[1][:-1])

print(output)

for i in range(len(newWords)):
    print(str(getError(output[i])))

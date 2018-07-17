from collections import OrderedDict
import re

# import geneticAlgo

#------------------------
# shared variables:
#------------------------

outputFilename = 'output.txt'

filename1 = 'data.txt'

allophones = {
    'aeiou' : 'a',
    'bp' : 'b',
    'cjsz' : 'z',
    'dt' : 'd',
    'fv' : 'v',
    'gkq' : 'g',
    'hx' : 'h',
    'lr' : 'l',
    'mn' : 'm',
    'w' : 'w',
    'y' : 'y'
    }

#------------------------
# functions:
#------------------------

def getFirstConsonantClusterAndVowel(word):
    output = ''
    for i in range(len(word)):
        char = word[i]
        if char not in 'aeiou':
            output += char
        elif i > 0:
            output += char
            return output
    if output == '' and len(word) > 0:
        output = word[0]
    return output

def getFirstConsonantClusterAndVowel_ofEachWord(words):
    for language in words:
        if language != 'Eng':
            words[language] = getFirstConsonantClusterAndVowel(words[language])
    return words

def getOrder(lang):
    if lang == 'Chi':
        return 1
    elif lang == 'Spa':
        return 2
    elif lang == 'Hin':
        return 3
    elif lang == 'Ara':
        return 4
    elif lang == 'Rus':
        return 5

def getAlloWord(word):
    alloWord = ''
    for letter in word:
        for allophoneGroup in allophones:
            if letter in allophoneGroup:
                alloWord += allophones[allophoneGroup]
    return alloWord

def removeRepeatingAlloWords(words):
    for lang1 in words:
        for lang2 in words:
            notSameWord = lang1 != lang2
            notEng = lang1 != 'Eng' and lang2 != 'Eng'
            notCompareWithNone = words[lang1] != '' and words[lang2] != ''
            if notSameWord and notEng and notCompareWithNone:
                if getOrder(lang2) > getOrder(lang1):
                    allo1 = getAlloWord(words[lang1])
                    allo2 = getAlloWord(words[lang2])
                    if allo2 in allo1:
                        words[lang2] = ''
    return words

def concatShortenedWords(words):
    newWord = ''
    for language in words:
        if language != 'Eng':
            newWord += words[language]
    return newWord

def createWord(words):
    newWord = ''
    words = getFirstConsonantClusterAndVowel_ofEachWord(words)
    words = removeRepeatingAlloWords(words)
    newWord = concatShortenedWords(words)
    return newWord

#------------------------
# main part of the program:
#------------------------

words = OrderedDict()
words['Eng'] = ''
words['Chi'] = ''
words['Spa'] = ''
words['Hin'] = ''
words['Ara'] = ''
words['Rus'] = ''

# get lines of file into a list:
with open(filename1,'r') as f1:
    data = f1.readlines()

with open(outputFilename,'a') as f2:
    f2.write('____________________\n')

# fill arrays:
for line in data:
    words['Eng'] = line.split(',')[1]
    words['Chi'] = line.split(',')[2]
    words['Spa'] = line.split(',')[3]
    words['Hin'] = line.split(',')[4]
    words['Ara'] = line.split(',')[5]
    words['Rus'] = line.split(',')[6]
    originalWords = words.copy()
    if words['Eng'] != 'Eng':
        newWord = createWord(words) # here is the major function call!
        with open(outputFilename,'a') as f2:
            f2.write(newWord + ',' + originalWords['Eng'] + ',' + originalWords['Chi'] + ',' + originalWords['Spa'] + ',' + originalWords['Hin'] + ',' + originalWords['Ara'] + ',' + originalWords['Rus'] + ',\n')

with open(outputFilename,'a') as f2:
    f2.write('____________________\n')

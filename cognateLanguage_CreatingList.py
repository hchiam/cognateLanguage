import time;

#------------------------
# shared variables:
#------------------------

words = {'Eng' : '', 'Chi' : '', 'Ara' : '', 'Spa' : '', 'Hin' : '', 'Rus' : ''}

outputFilename = 'output.txt'

filename1 = 'data.txt'

localtime = time.asctime(time.localtime(time.time()))

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

def respellWithInitialVowelAndConsonants(word):
    for char in word[1:]:
        if char in 'aeiou':
            word = word[0] + word[1:].replace(char,'')
    return word


def respellWithAllophones(word):
    for char in word:
        for allo in allophones:
            if char in allo:
                word = word.replace(char,allophones[allo])
    return word


def combineOverlappingWords(shortList):
    for language in shortList:
        for otherlanguage in shortList:
            if language != otherlanguage and language != 'Eng' and otherlanguage != 'Eng':
                a = shortList[language]
                b = shortList[otherlanguage]
                for i in range(1, len(b)):
                    if a.endswith(b[:i]):
                        shortList[otherlanguage] = ''
                        shortList[language] = a+b[i:]
    return shortList


def createWord():
    
    # function variables:

    originalWords = words
    wordsMinusNoninitialVowels = words
    shortList = []
    newWord = ''
    originalWords = words.copy() # must explicitly make copy of dictionary in Python (instead of a reference)
    
    # the words spelt with just the initial vowel and consonants:

    for language in words:
        if language != 'Eng':
            words[language] = respellWithInitialVowelAndConsonants(words[language])

    wordsMinusNoninitialVowels = words.copy() # must explicitly make copy of dictionary in Python (instead of a reference)

    # the words with allophonic spelling:

    for language in words:
        if language != 'Eng':
            words[language] = respellWithAllophones(words[language])

    # ignore repeats:

    shortList = words

    for language in shortList:
        for otherlanguage in shortList:
            if language != otherlanguage:
                if shortList[language] == shortList[otherlanguage]:
                    shortList[otherlanguage] = ''

    # ignore words embedded in other words:

    for language in shortList:
        for otherlanguage in shortList:
            if language != otherlanguage:
                if shortList[language] in shortList[otherlanguage]:
                    shortList[language] = ''

    # find overlaps in words:

    for tries in range(5):

        shortList = combineOverlappingWords(shortList)

    # append remaining words:

    for language in shortList:
        if language != 'Eng':
            newWord += shortList[language]


    # put original consonants back in, using 1st letters of higher-priority words:
    for language in reversed(words.keys()):
        if language != 'Eng':
            patternCompressedAllo = respellWithAllophones(wordsMinusNoninitialVowels[language])
            if wordsMinusNoninitialVowels[language] not in newWord:
                if patternCompressedAllo in respellWithAllophones(newWord): # replace with compressed word in allophone form
                    index = respellWithAllophones(newWord).find(patternCompressedAllo)
                    newWord = newWord[:index] + wordsMinusNoninitialVowels[language] + newWord[index+len(patternCompressedAllo):]
                else:
                    pattern = respellWithAllophones(wordsMinusNoninitialVowels[language])
                    newWord = newWord.replace(pattern, wordsMinusNoninitialVowels[language])

    # put original vowels (& consonants) back in, favouring higher-priority words:
    for language in reversed(words.keys()):
        if language != 'Eng':
            if originalWords[language] not in newWord:
                replacer = originalWords[language]
                # types of patterns:  (priorities: original word in allophonic form > compressed word in allophonic form > compressed original word, to enable vowel overwrites)
                patternOrigAllo = respellWithAllophones(originalWords[language])
                patternCompressedAllo = respellWithAllophones(wordsMinusNoninitialVowels[language])
                patternOrigCompressed = wordsMinusNoninitialVowels[language]
                tempWord = newWord
                # check if allophones exist that can be replaced, before checking for replacing compressed original word:
                if patternOrigAllo in respellWithAllophones(newWord):
                    index = respellWithAllophones(newWord).find(patternOrigAllo)
                    newWord = newWord[:index] + replacer + newWord[index+len(patternOrigAllo):]
                elif patternCompressedAllo in respellWithAllophones(newWord):
                    index = respellWithAllophones(newWord).find(patternCompressedAllo)
                    newWord = newWord[:index] + replacer + newWord[index+len(patternCompressedAllo):]
                else:
                    newWord = newWord.replace(patternOrigCompressed, replacer,1)

    print newWord
    return newWord

#------------------------
# main part of the program:
#------------------------

# get lines of file into a list:
with open(filename1,'r') as f1:
    data = f1.readlines()

with open(outputFilename,'a') as f2:
    f2.write('____________________\n')
    f2.write(localtime + '\n')

# fill arrays:
for line in data:
    words['Eng'] = line.split(',')[1]
    words['Chi'] = line.split(',')[2]
    words['Ara'] = line.split(',')[3]
    words['Spa'] = line.split(',')[4]
    words['Hin'] = line.split(',')[5]
    words['Rus'] = line.split(',')[6]
    if words['Eng'] != 'Eng':
        newWord = createWord() # here is the major function call!
        with open(outputFilename,'a') as f2:
            f2.write(words['Eng'] + '\t' + newWord + '\n')

with open(outputFilename,'a') as f2:
    f2.write('____________________\n')


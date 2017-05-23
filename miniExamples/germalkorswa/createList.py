from collections import OrderedDict
import re

#------------------------
# shared variables:
#------------------------

words = OrderedDict()

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

    wordsMinusNoninitialVowels = words
    shortList = []
    newWord = ''
    
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
            if language != otherlanguage and language != 'Eng' and otherlanguage != 'Eng':
                if shortList[language] == shortList[otherlanguage]:
                    shortList[otherlanguage] = ''

    # ignore words embedded in other words:

    for language in shortList:
        for otherlanguage in shortList:
            if language != otherlanguage and language != 'Eng' and otherlanguage != 'Eng':
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
    print ()
    print (newWord)
    return newWord


def simpNonChiWordMaker(word):
    indexVowel = -1
    # find (next) vowel:
    for letter in word:
        if letter in 'aeiou':
            indexVowel = word.find(letter)
            break
    # if still have next letter after get first vowel, then get first one (consonant) after it:
    if indexVowel < len(word)-1:
        indexVowelConsonant = indexVowel + 1
        word = word[:1+indexVowelConsonant]
    return word


#def simpChiWordMaker(word):
#    word = simpNonChiWordMaker(word)
#    #print word,'before'
#    patterns = [r'[dt](\_[cjsz]){1}',r'(\_[^aeiou])+[wy]']
#    replacers = ['','']
#    if word[0] in 'aeiou':
#        word = word[1:]
#    for i, pattern in enumerate(patterns):
#        word = re.sub(pattern,replacers[i],word,1)
#        #print word,'after',pattern
#    return word
#
#
#def removeHForHin(word,lang):
#    if lang == 'Hin':
#        word = re.sub(r'(\_[^aeiou])+h','',word)
#    return word


def createWord_DummyTest():
    return 'abcd'


def createWord_Alternate():
    
    # function variables:
    
    words = originalWords.copy()
    shortList = []
    newWord = ''
    indexVowel = -1
    indexVowelConsonant = -1
    
    # use only 1 (simplified) syllable of each word (only one ending consonant if any), with no intial vowel
    # CCCVC if not Chi. / CVC if Chi.
    for lang in words:
        if lang != 'Eng':
            word = words[lang]
            if word != '' and (word[0] in 'aeiou'): # no initial vowel
                words[lang] = word[1:]
            #if lang != 'Chi': # get first, simplified syllable
            words[lang] = simpNonChiWordMaker(words[lang])
            #elif lang == 'Chi':
            #words[lang] = simpChiWordMaker(words[lang])
            print (word)
            #removeHForHin(word,lang)

    wordsInitSyllables = words.copy()
    
    # the words with allophonic spelling:

    for language in words:
        if language != 'Eng':
            words[language] = respellWithAllophones(words[language])

    # ignore repeats:

    shortList = words

    for language in shortList:
        for otherlanguage in shortList:
            if language != otherlanguage and language != 'Eng' and otherlanguage != 'Eng':
                if shortList[language] == shortList[otherlanguage]:
                    shortList[otherlanguage] = ''

    # ignore words embedded in other words:

    for language in shortList:
        for otherlanguage in shortList:
            if language != otherlanguage and language != 'Eng' and otherlanguage != 'Eng':
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
            patternCompressedAllo = respellWithAllophones(wordsInitSyllables[language])
            if wordsInitSyllables[language] not in newWord:
                if patternCompressedAllo in respellWithAllophones(newWord): # replace with compressed word in allophone form
                    index = respellWithAllophones(newWord).find(patternCompressedAllo)
                    if index == 0 and (originalWords[language][0] in 'aeiou'):
                        print ("head!!!")
                        newWord = originalWords[language][0] + wordsInitSyllables[language] + newWord[index+len(patternCompressedAllo):]
                    else:
                        newWord = newWord[:index] + wordsInitSyllables[language] + newWord[index+len(patternCompressedAllo):]
                else:
                    pattern = respellWithAllophones(wordsInitSyllables[language])
                    newWord = newWord.replace(pattern, wordsInitSyllables[language])

    print (newWord)
    return newWord

#------------------------
# main part of the program:
#------------------------

# get lines of file into a list:
with open(filename1,'r') as f1:
    data = f1.readlines()

# get language headers:
langs = data[0].replace(',\n','').split(',')[1:] # "0,Eng,...,...,...," -> "..., ..., ..." (no 'Eng' and no final comma or '\n')

# put those language headers into the ordered dictionary:
for lang in langs:
    words[lang] = ''

# fill arrays:
for line in data:
    i = 0
    for lang in words:
        i += 1
        words[lang] = line.split(',')[i]
    originalWords = words.copy()
    originalWords_Alt = words.copy()
    if words['Eng'] != 'Eng':
        newWord = createWord_Alternate() # here is the major function call!
        with open(outputFilename,'a') as f2:
            entry = newWord.strip()
            for lang in langs:
                entry += ',' + originalWords[lang]
            entry += ',\n'
            f2.write(entry)

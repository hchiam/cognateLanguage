from collections import OrderedDict

#------------------------
# variables:
#------------------------

words = OrderedDict()
words['Eng'] = ''
words['Chi'] = ''
words['Spa'] = ''
words['Hin'] = ''
words['Ara'] = ''
words['Rus'] = ''

originalWords = words

wordsMinusNoninitialVowels = words

shortList = []

newWord = ''

filename = 'data.txt'

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
# methods:
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

#------------------------
# main part of the program:
#------------------------

# get lines of file into a list:
with open(filename,'r') as fh:
    data = fh.readlines()

# fill arrays:
for line in data:
    words['Eng'] = line.split(',')[1]
    words['Chi'] = line.split(',')[2]
    words['Spa'] = line.split(',')[3]
    words['Hin'] = line.split(',')[4]
    words['Ara'] = line.split(',')[5]
    words['Rus'] = line.split(',')[6]
    if words['Eng'] == 'be':
        break # get rid of this break condition in later versions of code

originalWords = words.copy() # must explicitly make copy of dictionary in Python (instead of a reference)

# show the words:
print '\nshow the words:'

for language in words:
    if language != 'Eng':
        print language + '\t' + words[language]

# show the words spelt with just the initial vowel and consonants:
print '\nshow the words spelt with just the initial vowel and consonants:'

for language in words:
    if language != 'Eng':
        words[language] = respellWithInitialVowelAndConsonants(words[language])
        print language + '\t' + words[language]

wordsMinusNoninitialVowels = words.copy() # must explicitly make copy of dictionary in Python (instead of a reference)

# show the words with allophonic spelling:
print '\nshow the words with allophonic spelling:'

for language in words:
    if language != 'Eng':
        words[language] = respellWithAllophones(words[language])
        print language + '\t' + words[language]

# ignore repeats:
print '\nignore repeats:'

shortList = words

for language in shortList:
    for otherlanguage in shortList:
        if language != otherlanguage and language != 'Eng' and otherlanguage != 'Eng':
            if shortList[language] == shortList[otherlanguage]:
                shortList[otherlanguage] = ''

for language in shortList:
    if language != 'Eng':
        print language + '\t' + shortList[language] # print the unique words

# ignore words embedded in other words:
print '\nignore words embedded in other words:'

for language in shortList:
    for otherlanguage in shortList:
        if language != otherlanguage and language != 'Eng' and otherlanguage != 'Eng':
            if shortList[language] in shortList[otherlanguage]:
                shortList[language] = ''

for language in shortList:
    if language != 'Eng':
        print language + '\t' + shortList[language]

# find overlaps in words:

for tries in range(5):
    print '\nfind overlaps in words:  try #' + str(tries+1)

    shortList = combineOverlappingWords(shortList)

    for language in shortList:
        if language != 'Eng':
            print language + '\t' + shortList[language]

# append remaining words:
print '\nappend remaining words:'

for language in shortList:
    if language != 'Eng':
        newWord += shortList[language]

print newWord

# put original consonants back in, using 1st letters of higher-priority words:
print '\nput original consonants back in, using 1st letters of higher-priority words:'
#print
#print 'originalWords = \n', originalWords, '\n'
#print 'wordsMinusNoninitialVowels = \n', wordsMinusNoninitialVowels, '\n'
#print 'words = \n', words, '\n'
print words
for language in reversed(words.keys()):
    if language != 'Eng':
        print wordsMinusNoninitialVowels[language]
        patternCompressedAllo = respellWithAllophones(wordsMinusNoninitialVowels[language])
        if wordsMinusNoninitialVowels[language] not in newWord:
            if patternCompressedAllo in respellWithAllophones(newWord): # replace with compressed word in allophone form
                index = respellWithAllophones(newWord).find(patternCompressedAllo)
                newWord = newWord[:index] + wordsMinusNoninitialVowels[language] + newWord[index+len(patternCompressedAllo):]
                print ':', patternCompressedAllo
            else:
                pattern = respellWithAllophones(wordsMinusNoninitialVowels[language])
                newWord = newWord.replace(pattern, wordsMinusNoninitialVowels[language])
            print ' ->\t', newWord

print "\nnewWord = ", newWord

# put original vowels (& consonants) back in, favouring higher-priority words:
print '\nput original vowels (& consonants) back in, favouring higher-priority words:'
print originalWords
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
                print 'replace patternOrigAllo:'
                index = respellWithAllophones(newWord).find(patternOrigAllo)
                newWord = newWord[:index] + replacer + newWord[index+len(patternOrigAllo):]
            elif patternCompressedAllo in respellWithAllophones(newWord):
                print 'replace patternCompressedAllo:'
                index = respellWithAllophones(newWord).find(patternCompressedAllo)
                newWord = newWord[:index] + replacer + newWord[index+len(patternCompressedAllo):]
            else:
                print 'replace patternOrigCompressed:', patternOrigCompressed
                newWord = newWord.replace(patternOrigCompressed, replacer,1)
            print '\t', replacer, '\t->\t', newWord, '<changed>'

print "\nnewWord = ", newWord
print "\noriginal words = "
for language in words:
    if language != 'Eng':
        print language + '\t' + originalWords[language]



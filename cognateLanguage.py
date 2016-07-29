#------------------------
# variables:
#------------------------

words = {'Eng' : '', 'Chi' : '', 'Ara' : '', 'Spa' : '', 'Hin' : '', 'Rus' : ''}

originalWords = words

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

def combineOverlappingWords():
    for word in shortList:
        for otherWord in shortList:
            if word != otherWord and word != 'Eng' and otherWord != 'Eng':
                a = shortList[word]
                b = shortList[otherWord]
                for i in range(1, len(b)):
                    if a.endswith(b[:i]):
                        shortList[otherWord] = ''
                        shortList[word] = a+b[i:]
    for word in shortList:
        if word != 'Eng':
            print word + '\t' + shortList[word]

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
    words['Ara'] = line.split(',')[3]
    words['Spa'] = line.split(',')[4]
    words['Hin'] = line.split(',')[5]
    words['Rus'] = line.split(',')[6]
    if words['Eng'] == 'test2':
        break # get rid of this later

originalWords = words

# show the words:
print '\nshow the words:'

for word in words:
    if word != 'Eng':
        print word + '\t' + words[word]

# show the words spelt with just the initial vowel and consonants:
print '\nshow the words spelt with just the initial vowel and consonants:'

for word in words:
    if word != 'Eng':
        words[word] = respellWithInitialVowelAndConsonants(words[word])
        print word + '\t' + words[word]

# show the words with allophonic spelling:
print '\nshow the words with allophonic spelling:'

for word in words:
    if word != 'Eng':
        words[word] = respellWithAllophones(words[word])
        print word + '\t' + words[word]

# ignore repeats:
print '\nignore repeats:'

shortList = words

for word in shortList:
    for otherWord in shortList:
        if word != otherWord:
            if shortList[word] == shortList[otherWord]:
                shortList[otherWord] = ''

for word in shortList:
    if word != 'Eng':
        print word + '\t' + shortList[word] # print the unique words

# ignore words embedded in other words:
print '\nignore words embedded in other words:'

for word in shortList:
    for otherWord in shortList:
        if word != otherWord:
            if shortList[word] in shortList[otherWord]:
                shortList[word] = ''

for word in shortList:
    if word != 'Eng':
        print word + '\t' + shortList[word]

# find overlaps in words:
print '\nfind overlaps in words:'

combineOverlappingWords()

# find overlaps in words, x2:
print '\nfind overlaps in words, x2:'
combineOverlappingWords()

# find overlaps in words, x3:
print '\nfind overlaps in words, x3:'
combineOverlappingWords()

# find overlaps in words, x4:
print '\nfind overlaps in words, x4:'
combineOverlappingWords()

# append remaining words:
print '\nappend remaining words:'

for word in shortList:
    if word != 'Eng':
        newWord += shortList[word]

print newWord

# put original consonants back in, using 1st letters of higher-priority words:
print '\nput original consonants back in, using 1st letters of higher-priority words:'

print originalWords
print words







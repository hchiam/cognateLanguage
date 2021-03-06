from collections import Counter

def countCollisions(entries,filename='output_shortlist.txt'):
    collisions = [k for k,v in Counter(entries).items() if v>1]
    num_collisions = len(collisions)
    print('number of collisions: ' + str(num_collisions))

    with open(filename,'r') as f:
        for i, l in enumerate(f):
            pass
    numLines = i+1
    print('rate of collisions: ' + str(round(num_collisions * 100.0 / numLines, 2)) + ' %')

    print('word collisions: ' + str(collisions))
    return num_collisions

def countCollisionsInFile(filename,cv=False,cvc=False,allofinal=False,justCons=False):
    entries = []
    with open(filename,'r') as f:
        for line in f:
            # get just the output words
            entry = line.split(',')[0].replace(' \'','')
            if cv:
                entry = justTwoInitSylls_CV(entry)
            elif cvc:
                entry = justTwoInitSylls_CVC(entry)
            elif allofinal:
                entry = justTwoInitSylls_CVC_AlloFinal(entry)
            elif justCons:
                entry = justConsonants(entry)
            entries.append(entry)
    return countCollisions(entries,filename)

def countCollisionsInList(entries):
    return countCollisions(entries)

def justTwoInitSylls_CV(word):
    beforeThisIndex = 0
    afterThisIndex = 0
    for vowel1 in word:
        if vowel1 in 'aeiou':
            afterThisIndex = word.index(vowel1)
            break
    for vowel2 in word[afterThisIndex+1:]:
        if vowel2 in 'aeiou':
            beforeThisIndex = word[afterThisIndex+1:].index(vowel2)+1 + afterThisIndex+1
            break
    if beforeThisIndex!=0:
        word = word[:beforeThisIndex]
    return word

def justTwoInitSylls_CVC(word):
    beforeThisIndex = 0
    afterThisIndex = 0
    for vowel1 in word:
        if vowel1 in 'aeiou':
            afterThisIndex = word.index(vowel1)
            break
    for vowel2 in word[afterThisIndex+1:]:
        if vowel2 in 'aeiou':
            beforeThisIndex = word[afterThisIndex+1:].index(vowel2)+1 + afterThisIndex+1
            break
    if beforeThisIndex!=0:
        word = word[:beforeThisIndex+1]
    return word

def justTwoInitSylls_CVC_AlloFinal(word):
    word = list(justTwoInitSylls_CVC(word))
    allophones = {
        'e':'a', 'i':'a', 'o':'a', 'u':'a',
        'p':'b',
        'c':'z', 'j':'z', 's':'z',
        't':'d',
        'f':'v',
        'k':'g', 'q':'g',
        'x':'h',
        'r':'l',
        'n':'m'
    }
    if word[-1] in allophones:
        word[-1] = allophones[word[-1]]
    return ''.join(word)

def justConsonants(word):
    word = list(justTwoInitSylls_CVC(word))
    vowels = {'a':'','e':'','i':'','o':'','u':''}
    startIndex = 0
    if word[0] in vowels:
        startIndex = 1
    for i in range(startIndex,len(word)):
        letter = word[i]
        if letter in vowels:
            word[i] = vowels[letter]
    return ''.join(word)

if __name__ == '__main__': # if running this .py file directly
    fileName = 'output_shortlist.txt'
    print('\n--- whole words: ---')
    countCollisionsInFile(fileName)
    print('\n--- cv: 1st 2 syllables: ---')
    countCollisionsInFile(fileName,cv=True)
    print('\n--- cvc: 1st 2 syllables: ---')
    countCollisionsInFile(fileName,cvc=True)
    print('\n--- cvc : 1st 2 syllables + ALLO FINAL: ---')
    countCollisionsInFile(fileName,allofinal=True)
    print('\n--- cvc : 1st 2 syllables + CONSONANTS ONLY: ---')
    countCollisionsInFile(fileName,justCons=True)

from collections import Counter

def countCollisions(entries):
    collisions = [k for k,v in Counter(entries).items() if v>1]
    num_collisions = len(collisions)
    print('word collisions:' + str(num_collisions) + '\n' + str(collisions))
    return num_collisions

def countCollisionsInFile(filename,cv=False,cvc=False):
    entries = []
    with open(filename,'r') as f:
        for line in f:
            # get just the output words
            entry = line.split(',')[0].replace(' \'','')
            if cv:
                entry = justTwoInitSylls_CV(entry)
            elif cvc:
                entry = justTwoInitSylls_CVC(entry)
            entries.append(entry)
    return countCollisions(entries)

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

if __name__ == '__main__': # if running this .py file directly
    fileName = 'output_shortlist.txt'
    print('\n--- whole words: ---')
    countCollisionsInFile(fileName)
    print('\n--- cv: 1st 2 syllables: ---')
    countCollisionsInFile(fileName,cv=True)
    print('\n--- cvc: 1st 2 syllables: ---')
    countCollisionsInFile(fileName,cvc=True)

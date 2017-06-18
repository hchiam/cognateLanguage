from findCollisions import countCollisionsInList

data = []

def getData(cvc=False,cv=False):
    inputFile = 'output_shortlist.txt'
    data = []
    with open(inputFile,'r') as f1:
        for line in f1:
            word = line.split(',')[0]
            if cvc:
                word = justTwoInitSylls_CVC(word)
            elif cv:
                word = justTwoInitSylls_CV(word)
            data.append(word)
    return data

def justTwoInitSylls_CVC(word):
    beforeThisIndex = 0
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

def justTwoInitSylls_CV(word):
    beforeThisIndex = 0
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

def compare_CVC_vs_CV():
    print('____________________\nCVC:')
    data = getData(cvc=True)
    collisions_cvc = countCollisionsInList(data)
    print('____________________\nCV:')
    data = getData(cv=True)
    collisions_cv = countCollisionsInList(data)
    print('____________________\nWant less collisions?')
    if collisions_cvc < collisions_cv:
        print('Go with CVC')
    elif collisions_cv < collisions_cvc:
        print('Go with CV')
    else:
        print('There\'s no difference between CVC and CV.')

compare_CVC_vs_CV()

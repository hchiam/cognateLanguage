from collections import OrderedDict

#------------------------
# shared variables:
#------------------------

words = OrderedDict()
words['Eng'] = ''
words['Chi'] = ''
words['Ara'] = ''
words['Spa'] = ''
words['Hin'] = ''
words['Rus'] = ''

outputFilename = 'output.txt'

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


def evaluateScore1(word,chi,ara,spa,hin,rus):
    score = 0
    
    scoreLangs = [0,0,0,0,0]
    
    leastEfficientWord = chi+ara+spa+hin+rus
    print '\n'
    print 'Least Efficient Word = ', leastEfficientWord
    print 'Evaluated Word = ', word
    
    # ABZDAVG allo w/ vowels
    
    alloWithVowels = respellWithAllophones(word)
    print 'Allophone Form of Word, with Vowels: ', alloWithVowels
    
    originalWords = [chi,ara,spa,hin,rus]
    alloOriginalWords = originalWords
    
    for index, srcWord in enumerate(alloOriginalWords):
        alloOriginalWords[index] = respellWithAllophones(srcWord)
    
    print alloOriginalWords

    # get preliminary scores for each language:
    for lang, srcWordAllo in enumerate(alloOriginalWords):
        for i in range(len(srcWordAllo)):
            head = srcWordAllo[:i]
            if head in respellWithAllophones(word):
                # add to score per matching letter of word:
                scoreLangs[lang] += 1
    
    # adjust language scores by number of characters in original words:
    for lang, srcWordAllo in enumerate(alloOriginalWords):
        scoreLangs[lang] -= len(srcWordAllo)

    # language scores are weighted in reverse order
    scoreLangs.reverse()

    for wt, lang in enumerate(scoreLangs):
        score += lang + lang * (wt/10.0) # make weightings like these to make gradient of influence:  0.1, 0.2, 0.3, 0.4, 0.5
    #print 'language score contribution: ', score
    
    # get preliminary score for word length:
    scoreLen = (len(leastEfficientWord) - len(word)) # score increases with shorter word
    scoreLen *= 1.1 # this is the weighting for length score
    #print 'word length contribution', scoreLen
    score += scoreLen

    return score


def evaluateScore2(word,chi,ara,spa,hin,rus):
    score = 0
    # insert code here
    # ABZDVG
    return score

#------------------------
# main part of the program:
#------------------------

# get lines of file into a list:
with open(outputFilename,'r') as f1:
    data = f1.readlines()

# fill arrays:
for line in data:
    if ',' in line:
        word = line.split(',')[0]
        words['Chi'] = line.split(',')[2]
        words['Ara'] = line.split(',')[3]
        words['Spa'] = line.split(',')[4]
        words['Hin'] = line.split(',')[5]
        words['Rus'] = line.split(',')[6]
        score = evaluateScore1(word,words['Chi'],words['Ara'],words['Spa'],words['Hin'],words['Rus']) # here is the major function call!
        print word, '-> evaluator 1: ', score
        score = evaluateScore2(word,words['Chi'],words['Ara'],words['Spa'],words['Hin'],words['Rus']) # here is the major function call!
        print word, '-> evaluator 2: ', score



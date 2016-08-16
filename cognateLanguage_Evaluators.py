from collections import OrderedDict
from levenshteinDistance import levenshtein as ld

#------------------------
# shared variables:
#------------------------

words = OrderedDict()
words['Eng'] = ''
words['Chi'] = ''
words['Spa'] = ''
words['Hin'] = ''
words['Ara'] = ''
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


def evaluateScore_Levenshtein(word,chi,spa,hin,ara,rus):
    score = 0
    
    for lang in chi,spa,hin,ara,rus:
        score += ld(word,lang)
    
    return score


def evaluateScore_AlloWithVowels(word,chi,spa,hin,ara,rus):
    score = 0
    scoreLangs = [0,0,0,0,0]
    
    leastEfficientWord = chi+spa+hin+ara+rus
    
    # ABZDAVG allo w/ vowels
    
    alloWithVowels = respellWithAllophones(word)
    #print 'Allophone Form of Word, with Vowels: ', alloWithVowels
    
    originalWords = [chi,spa,hin,ara,rus]
    alloOriginalWords = originalWords
    
    for index, srcWord in enumerate(alloOriginalWords):
        alloOriginalWords[index] = respellWithAllophones(srcWord)
    
    #print alloOriginalWords

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
        score += lang + lang * ((wt+1)/10.0) # make weightings like these to make gradient of influence:  0.1, 0.2, 0.3, 0.4, 0.5
    #print 'language score contribution: ', score
    
    # get preliminary score for word length:
    scoreLen = (len(leastEfficientWord) - len(word)) # score increases with shorter word
    scoreLen *= 1.1 # this is the weighting for length score
    #print 'word length contribution', scoreLen
    score += scoreLen

    return score


def evaluateScore_ConsonantsInOrder(word,chi,spa,hin,ara,rus):
    score = 0
    scoreLangs = [0,0,0,0,0]
    
    leastEfficientWord = chi+spa+hin+ara+rus
    
    originalWords = [chi,spa,hin,ara,rus]
    alloConsonants = originalWords
    alloOfNewWord = respellWithAllophones(word).replace('a','').replace('e','').replace('i','').replace('o','').replace('u','')
    
    #print alloOfNewWord
    
    for index, srcWord in enumerate(alloConsonants):
        alloConsonants[index] = respellWithAllophones(srcWord).replace('a','').replace('e','').replace('i','').replace('o','').replace('u','')
    
    #print alloConsonants
    
    # BZDVG
    
    # go through each language's test pattern:
    for lang, testPattern in enumerate(alloConsonants):
        currentLetterPos = 0
        # go through as many letters of that test pattern as possible:
        for i in range(1,len(testPattern)):
            # if that letter is found in new word then update current letter position (= index+1 since list indices start at 0):
            if testPattern[i] in alloOfNewWord:
                #print testPattern[i]
                currentLetterPos = i+1
        # use full word length - the current letter into the test pattern as the score for that language
        scoreLangs[lang] = currentLetterPos - len(originalWords[lang])
        currentLetterPos = 0
        #print scoreLangs

    # language scores are weighted in reverse order
    scoreLangs.reverse()

    for wt, lang in enumerate(scoreLangs):
        score += lang + lang * ((wt+1)/10.0) # make weightings like these to make gradient of influence:  0.1, 0.2, 0.3, 0.4, 0.5

    # get preliminary score for word length:
    scoreLen = (len(leastEfficientWord) - len(word)) # score increases with shorter word
    scoreLen *= 1.1 # this is the weighting for length score
    #print 'word length contribution', scoreLen
    score += scoreLen
    
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
        newWord = line.split(',')[0]
        words['Chi'] = line.split(',')[2]
        words['Spa'] = line.split(',')[3]
        words['Hin'] = line.split(',')[4]
        words['Ara'] = line.split(',')[5]
        words['Rus'] = line.split(',')[6]
        originalWords = [words['Chi'], words['Spa'], words['Hin'], words['Ara'], words['Rus']]
        leastEfficientWord = words['Chi'] + words['Spa'] + words['Hin'] + words['Ara'] + words['Rus']
        print '\n'
        print newWord.upper() + ' vs. "' + leastEfficientWord + '":'
        print originalWords
        score1 = evaluateScore_AlloWithVowels(newWord, words['Chi'],words['Spa'],words['Hin'],words['Ara'],words['Rus'])
        print '  ' + str(score1) + '\t<- evaluateScore_AlloWithVowels'
        score2 = evaluateScore_ConsonantsInOrder(newWord, words['Chi'],words['Spa'],words['Hin'],words['Ara'],words['Rus'])
        print '  ' + str(score2) + '\t<- evaluateScore_ConsonantsInOrder'
        avgScore = (score1 + score2)/2
        print 'Average score: ' + str(avgScore)
        score3 = evaluateScore_Levenshtein(newWord, words['Chi'],words['Spa'],words['Hin'],words['Ara'],words['Rus'])
        print '\n  ' + str(score3) + '\t<- evaluateScore_Levenshtein'

print '\n'








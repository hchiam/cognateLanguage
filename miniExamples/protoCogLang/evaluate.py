from collections import OrderedDict
from levenshteinDistance import levenshtein as ld

#------------------------
# shared variables:
#------------------------

words = OrderedDict()
words['Eng'] = ''
words['pie'] = ''
words['pa'] = ''
words['pii'] = ''
words['pbs'] = ''
words['ps'] = ''

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


def evaluateScore_Levenshtein(word,originalWords):
    score = 0
    score_maximize = 100 # just to keep score positive
    score_minimize = 0
    
    for lang in originalWords:
        score_minimize += ld(word,lang)
    
    score = score_maximize - score_minimize
    
    return score


def evaluateScore_AlloWithVowels(word,originalWords):
    score = 0
    scoreLangs = [0] * len(originalWords)
    
    leastEfficientWord = ''.join(originalWords)
    
    # ABZDAVG allo w/ vowels
    
    alloWithVowels = respellWithAllophones(word)
    #print 'Allophone Form of Word, with Vowels: ', alloWithVowels
    
    alloOriginalWords = list(originalWords) # careful with creating references that overwrite!
    
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

    return round(score,2)


def evaluateScore_ConsonantsInOrder(word,originalWords):
    score = 0
    scoreLangs = [0] * len(originalWords)
    
    leastEfficientWord = ''.join(originalWords)
    
    alloConsonants = list(originalWords) # careful with creating references that overwrite!
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
    
    return round(score,2)


def evaluateScore_LettersFromEachSource(word,originalWords):
    score = 0
    for letter in word:
        for srcWord in originalWords:
            # encourage using words with letters found in all source words
            score += 1 if letter in srcWord else 0
    return score


def penalizeRepeatedLetterSequences(word):
    score = 0
    currentLetter = ''
    for letter in word:
        if letter == currentLetter:
            score -= 1
        else:
            currentLetter = letter
    return score


def penalizeLength(word):
    score = -len(word)
    return score


def evaluate(line):
    newWord = line.split(',')[0]
    originalWords = line.split(',')[2:]
    
    score = 0
    score += evaluateScore_AlloWithVowels(newWord, originalWords)
    score += evaluateScore_ConsonantsInOrder(newWord, originalWords)
    score += evaluateScore_Levenshtein(newWord, originalWords)
    score += evaluateScore_LettersFromEachSource(newWord, originalWords)
    score += penalizeRepeatedLetterSequences(newWord)
    score += penalizeLength(newWord)
    return round(score, 2)

#------------------------
# main part of the program:
#------------------------

# get lines of file into a list:
with open(outputFilename,'r') as f1:
    data = f1.readlines()

# fill arrays:
for line in data:
    if ',' in line:
        print(evaluate(line))

from random import randint
from operator import itemgetter

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


def evaluateScore_Levenshtein(word,a,b,c,d,e):
    score = 0
    
    for lang in a,b,c,d,e:
        score += ld(word,lang)
    
    return score


def evaluateScore_AlloWithVowels(word,a,b,c,d,e):
    score = 0
    scoreLangs = [0,0,0,0,0]
    
    leastEfficientWord = a+b+c+d+e
    
    # ABZDAVG allo w/ vowels
    
    alloWithVowels = respellWithAllophones(word)
    #print 'Allophone Form of Word, with Vowels: ', alloWithVowels
    
    originalWords = [a,b,c,d,e]
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

    return round(score,2)


def evaluateScore_ConsonantsInOrder(word,a,b,c,d,e):
    score = 0
    scoreLangs = [0,0,0,0,0]
    
    leastEfficientWord = a+b+c+d+e
    
    originalWords = [a,b,c,d,e]
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
    
    return round(score,2)

def evaluate(line):
    newWord = line.split(',')[0]
    words['pie'] = line.split(',')[2]
    words['pa'] = line.split(',')[3]
    words['pii'] = line.split(',')[4]
    words['pbs'] = line.split(',')[5]
    words['ps'] = line.split(',')[6]
    originalWords = [words['pie'], words['pa'], words['pii'], words['pbs'], words['ps']]
    leastEfficientWord = words['pie'] + words['pa'] + words['pii'] + words['pbs'] + words['ps']
    score1 = evaluateScore_AlloWithVowels(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    score2 = evaluateScore_ConsonantsInOrder(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    # score3 = evaluateScore_Levenshtein(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    # scoreSum = score1+score2-score3
    scoreSum = (score1+score2)/2
    scoreSum = score1+score2
    return round(scoreSum, 2)

def getSourceWords(data):
    return data.split(',')[2:][:-1]

def generateNewIndividual():
    outputInstructions = []
    # possibleInstructions = [0,1,2,3,4,'+','+','x'] # make '+' more likely (heuristically seems good)
    for i in range(25):
        index = randint(0,len(possibleInstructions)-1)
        instruction = possibleInstructions[index]
        if instruction == 'x':
            if outputInstructions != '':
                break
        else:
            outputInstructions.append(instruction)
    return outputInstructions

def generateNewWord(data, instructions):
    newWord = []
    sourceWords = data
    i = 0
    for instruction in instructions:
        if instruction == '+':
            i += 1
        else:
            sourceWord = sourceWords[instruction]
            if i < len(sourceWord):
                newWord.append(sourceWord[i])
    newWord = ''.join(newWord)
    return newWord

def sortByScore(population):
    population.sort(key=itemgetter(0), reverse=True)

def printOnSepLines(arr):
    for line in arr:
        print(line)

#------------------------
# main part of the program:
#------------------------

data = '+,long,tcan,largo,lamba,towil,dlini,' # tcanlartowdlam

possibleInstructions = [0,1,2,3,4,'+','+','x'] # make '+' more likely (heuristically seems good)

population = []

srcWords = getSourceWords(data)

# initialize population
for i in range(10):
    instructions = generateNewIndividual()
    newWord = generateNewWord(srcWords, instructions)
    entry = newWord + ',' + ','.join(srcWords) + ','
    score = evaluate(entry)
    individual = [score, entry, instructions]
    population.append(individual)

for i in range(500):
    # sort by score
    sortByScore(population)
    # printOnSepLines(population)
    
    # remove lower scorers
    for i in range(5):
        population.pop()
    
    # add new random individuals to population
    for i in range(3):
        instructions = generateNewIndividual()
        newWord = generateNewWord(srcWords, instructions)
        entry = newWord + ',' + ','.join(srcWords) + ','
        score = evaluate(entry)
        individual = [score, entry, instructions]
        population.append(individual)
    
    # add variations of existing individuals in population
    for i in range(2):
        index = randint(0,len(population)-1)
        instructions_toMutate = population[index][2]
        if len(instructions_toMutate) > 0:
            # mutate instructions
            index_toMutate = randint(0,len(instructions_toMutate)-1)
            instruction_toReplace = possibleInstructions[ randint(0,len(possibleInstructions)-1) ]
            if instruction_toReplace != 'x':
                instructions_toMutate[index_toMutate] = instruction_toReplace
            else:
                instructions_toMutate = instructions_toMutate[index_toMutate-1:]
        else:
            instructions_toMutate = ''
        instructions = instructions_toMutate
        newWord = generateNewWord(srcWords, instructions)
        entry = newWord + ',,' + ','.join(srcWords) + ',' # should have 7 commas
        score = evaluate(entry)
        individual = [score, entry, instructions]
        population.append(individual)

# sort by score
sortByScore(population)
print('FINAL CANDIDATES:')
printOnSepLines(population)

from random import randint
from operator import itemgetter
import matplotlib.pyplot as plt

from collections import OrderedDict
# from levenshteinDistance import levenshtein as ld

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


# def evaluateScore_Levenshtein(word,a,b,c,d,e):
#     score = 0
#     
#     for lang in a,b,c,d,e:
#         score += ld(word,lang)
#     
#     return score


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

def evaluateScore_LettersFromEachSource(word,a,b,c,d,e):
    score = 0
    for letter in word:
        # encourage using words with letters found in all source words
        score += 1 if letter in a else 0
        score += 1 if letter in b else 0
        score += 1 if letter in c else 0
        score += 1 if letter in d else 0
        score += 1 if letter in e else 0
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
    words['pie'] = line.split(',')[2]
    words['pa'] = line.split(',')[3]
    words['pii'] = line.split(',')[4]
    words['pbs'] = line.split(',')[5]
    words['ps'] = line.split(',')[6]
    originalWords = [words['pie'], words['pa'], words['pii'], words['pbs'], words['ps']]
    
    score = 0
    score += evaluateScore_AlloWithVowels(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    score += evaluateScore_ConsonantsInOrder(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    # score -= evaluateScore_Levenshtein(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    score += evaluateScore_LettersFromEachSource(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    score += penalizeRepeatedLetterSequences(newWord)
    score += penalizeLength(newWord)
    return round(score, 2)

def evaluate_OLD(line):
    newWord = line.split(',')[0]
    words['pie'] = line.split(',')[2]
    words['pa'] = line.split(',')[3]
    words['pii'] = line.split(',')[4]
    words['pbs'] = line.split(',')[5]
    words['ps'] = line.split(',')[6]
    originalWords = [words['pie'], words['pa'], words['pii'], words['pbs'], words['ps']]
    
    score = 0
    score += evaluateScore_AlloWithVowels(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    score += evaluateScore_ConsonantsInOrder(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    # score -= evaluateScore_Levenshtein(newWord, words['pie'], words['pa'], words['pii'], words['pbs'], words['ps'])
    return round(score, 2)

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

def generateNewWord(srcWords, instructions):
    newWord = []
    sourceWords = srcWords
    i = 0
    for instruction in instructions:
        if instruction == 'x':
            break
        elif instruction == '+':
            i += 1
        else:
            sourceWord = sourceWords[instruction]
            if i < len(sourceWord):
                newWord.append(sourceWord[i])
    newWord = ''.join(newWord)
    return newWord

def sortByScore(population):
    population.sort(key=itemgetter(0), reverse=True)

def getBestAlgo():
    # assumes first one is best
    bestSoFar = population[0]
    return bestSoFar

def printOnSepLines(arr):
    for line in arr:
        print(line)

def updateScoreHistory():
    # assumes first one is best
    currentBestScore = population[0][0]
    scoreHistory.append(currentBestScore)

#------------------------
# main part of the program:
#------------------------

possibleInstructions = [0,1,2,3,4,'+','+','x'] # make '+' more likely (heuristically seems good)

# data = '+,long,tcan,largo,lamba,towil,dlini,' # tcanlartowdlam
data = '0,use,yun,usa,istemal,istemal,potrebi,' # yunsastempot
srcWords = getSourceWords(data)
engWord = data.split(',')[1]

popSize = 10
population = []
scoreHistory = []

# initialize population
for i in range(popSize):
    instructions = generateNewIndividual()
    newWord = generateNewWord(srcWords, instructions)
    entry = newWord + ',' + ','.join(srcWords) + ','
    score = evaluate(entry)
    individual = [score, entry, instructions]
    population.append(individual)

updateScoreHistory()

# train
for i in range(500):
    # sort by score
    sortByScore(population)
    # printOnSepLines(population)
    
    # update score history after sorting by score
    updateScoreHistory()
    
    # remove lower scorers
    halfOfPop = popSize//2
    for i in range(halfOfPop):
        population.pop()
    
    # add new random individuals to population
    halfOfHalf = halfOfPop//2
    for i in range(halfOfHalf):
        instructions = generateNewIndividual()
        newWord = generateNewWord(srcWords, instructions)
        entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
        score = evaluate(entry)
        individual = [score, entry, instructions]
        population.append(individual)
    
    # remove duplicate individuals
    mySet = []
    for indiv in population:
        if indiv not in mySet:
            mySet.append(indiv)
    duplicatesToReplace = len(population) - len(mySet)
    population = list(mySet)
    
    # add variations of existing individuals in population
    restOfPop = halfOfPop - halfOfHalf + duplicatesToReplace
    for i in range(restOfPop):
        index = randint(0,len(population)-1)
        instructions_toMutate = list(population[index][2]) # hacky: use list() to make an actual copy, not a reference
        if len(instructions_toMutate) > 0:
            for i in range(3):
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
        entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
        score = evaluate(entry)
        individual = [score, entry, instructions]
        population.append(individual)

# sort by score
sortByScore(population)
print('\nFINAL CANDIDATES:')
printOnSepLines(population)

# save the best so far
bestSoFar = getBestAlgo()
scoreBestSoFar, entryBestSoFar, instructionsBestSoFar = bestSoFar
print('\nBEST SO FAR:')
print(bestSoFar)

print('\nORIGINALLY:')
original = 'yunsastempot,use,yun,usa,istemal,istemal,potrebi,'
# original = 'tcanlartowdlam,long,tcan,largo,lamba,towil,dlini,'
print(evaluate(original), original)

print('\nIF USE BEST SO FAR ON DIFFERENT INPUT:')
data = '+,long,tcan,largo,lamba,towil,dlini,' # can use this to check still outputs same newWord
# data = '0,use,yun,usa,istemal,istemal,potrebi,'
srcWords = getSourceWords(data)
engWord = data.split(',')[1]
newWord = generateNewWord(srcWords, instructionsBestSoFar)
entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
score = evaluate(entry)
individual = [score, entry, instructionsBestSoFar]
print(individual)

original = 'tcanlartowdlam,long,tcan,largo,lamba,towil,dlini,'
print('vs')
print(evaluate(original), original)

# plot score over generations
plt.plot(scoreHistory)
plt.show()

# TODO train over multiple examples

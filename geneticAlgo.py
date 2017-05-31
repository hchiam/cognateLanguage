from random import randint
from operator import itemgetter
# import matplotlib.pyplot as plt

# from collections import OrderedDict
from levenshteinDistance import levenshtein as ld

#------------------------
# shared variables:
#------------------------

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

possibleInstructions = [0,1,2,3,4,'+','+','x'] # make '+' more likely (heuristically seems good)

popSize = 10
numGenerations = 1000
epochMilestone = numGenerations//10
population = []
scoreHistory = []
wordHistory = []

debugOn = False

count = 0

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
    
    for lang in originalWords:
        score += ld(word,lang)
    
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
    # need all of the following to avoid crazy long words with repeating letters
    score -= evaluateScore_Levenshtein(newWord, originalWords)
    score += evaluateScore_LettersFromEachSource(newWord, originalWords)
    score += penalizeRepeatedLetterSequences(newWord)
    score += penalizeLength(newWord)
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
    if debugOn:
        for line in arr:
            print(line)


def updateScoreHistory():
    # assumes first one is best
    currentBestScore = population[0][0]
    scoreHistory.append(currentBestScore)


def updateWordHistory():
    wordHistory.append(population[0][1].split(',',1)[0])


def getEntryIdentifier(entry):
    parts = str(entry).split(', ')
    sourceWordsListStr = parts[1]
    justSrcWords = sourceWordsListStr.split(',',1)[1]
    removedFinalApostrophe = justSrcWords[:-1]
    identifier = removedFinalApostrophe
    return identifier


def getEntryScore(entry):
    return str(entry).split(', ',1)[0][1:] # [1:] to remove initial '['


def printDebug(*args):
    if debugOn:
        print(args)

#------------------------
# main part of the program:
#------------------------

def createWord(inputLineEntry):
    global population
    global scoreHistory
    global wordHistory
    global count
    
    printDebug('\n...Running...')
    count += 1
    print(count)
    
    # data = '+,long,tcan,largo,lamba,towil,dlini,' # tcanlartowdlam
    # data = '0,use,yun,usa,istemal,istemal,potrebi,' # yunsastempot
    data = inputLineEntry
    srcWords = getSourceWords(data)
    engWord = data.split(',')[1]
    
    population = []
    scoreHistory = []
    wordHistory = []
    
    # initialize population
    for i in range(popSize):
        instructions = generateNewIndividual()
        newWord = generateNewWord(srcWords, instructions)
        entry = newWord + ',' + ','.join(srcWords) + ','
        score = evaluate(entry)
        individual = [score, entry, instructions]
        population.append(individual)
    
    # train
    for i in range(numGenerations):
        # sort by score
        sortByScore(population)
        # printOnSepLines(population)
        
        # update score history after sorting by score
        updateScoreHistory()
        
        # update word history after sorting by score
        if i%epochMilestone == 0:
            updateWordHistory()
        
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
    printDebug('\nFINAL CANDIDATES:')
    printOnSepLines(population)
    
    # get the best so far
    bestSoFar = getBestAlgo()
    scoreBestSoFar, entryBestSoFar, instructionsBestSoFar = bestSoFar
    printDebug('\nBEST SO FAR:')
    printDebug(bestSoFar)
    
    printDebug('\nORIGINALLY:')
    original = 'yunsastempot,use,yun,usa,istemal,istemal,potrebi,'
    # original = 'tcanlartowdlam,long,tcan,largo,lamba,towil,dlini,'
    printDebug(evaluate(original), original)
    
    printDebug('\nIF USE BEST SO FAR ON DIFFERENT INPUT:')
    data = '+,long,tcan,largo,lamba,towil,dlini,' # can use this to check still outputs same newWord
    # data = '0,use,yun,usa,istemal,istemal,potrebi,'
    srcWords = getSourceWords(data)
    engWord = data.split(',')[1]
    newWord = generateNewWord(srcWords, instructionsBestSoFar)
    entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
    score = evaluate(entry)
    individual = [score, entry, instructionsBestSoFar]
    printDebug(individual)
    
    original = 'tcanlartowdlam,long,tcan,largo,lamba,towil,dlini,'
    printDebug('vs')
    printDebug(evaluate(original), original)
    
    # show word history
    printDebug('\nBEST SCORERS AT EVERY '+str(epochMilestone)+' GENERATIONS:')
    printDebug(wordHistory)
    
    # # plot score over generations
    # plt.plot(scoreHistory)
    # plt.title('Score History')
    # plt.show()
    
    # save best scorer externally
    scorersFile = 'best-scorers.txt'
    scorers = []
    with open(scorersFile,'r') as f:
        scorers = f.read().splitlines()
    # f = open(scorersFile, 'r')
    # scorers = f.read().split('\n')
    # scorers = list(filter(None, scorers)) # remove empty lines
    # f.close()
    if scorers == []:
        # just initialize file if nothing there
        with open(scorersFile,'w') as f:
            f.write(str(bestSoFar)+'\n')
    else:
        bestSoFar_id = getEntryIdentifier(bestSoFar)
        bestSoFar_scr = getEntryScore(bestSoFar)
        bestSoFar_word = entryBestSoFar.split(',')[0].replace('\'','')
        
        all_prevScorer_ids = []
        for scorer in scorers:
            all_prevScorer_ids.append(getEntryIdentifier(scorer))
        
        newScorers = [] # reset
        
        if bestSoFar_id not in all_prevScorer_ids:
            # retain previous scorers
            for scorer in scorers:
                newScorers.append(scorer)
            # will add if new entry
            newScorers.append(bestSoFar)
        else:
            # check each line
            for scorer in scorers:
                prevScorer_id = getEntryIdentifier(scorer)
                if prevScorer_id == bestSoFar_id:
                    prevScorer_scr = getEntryScore(scorer)
                    # include only better scorer
                    if bestSoFar_scr > prevScorer_scr:
                        newScorers.append(bestSoFar)
                    else:
                        newScorers.append(scorer)
                        # replace with previously existing scorer as output word
                        bestSoFar_word = scorer.split(',')[1].replace(' \'','')
                else:
                    if scorer not in newScorers:
                        # otherwise make sure to include previously existing scorers
                        newScorers.append(scorer)
        with open(scorersFile,'w') as f:
            for scorer in newScorers: 
                f.write(str(scorer)+'\n')
            f.close()
    
    # TODO train over multiple examples
    
    return bestSoFar_word

if __name__ == '__main__': # run the following if running this .py file directly:
    inputLineEntry = '+,make,djidzaw,ase,bana,sana,dela,' # this one used to output 'abaaaaaasanlaaaaaaadaa'
    wordCreated = createWord(inputLineEntry)
    # inputLineEntry = '0,use,yun,usa,istemal,istemal,potrebi,' # yunsastempot
    # wordCreated = createWord(inputLineEntry)
    # inputLineEntry = '+,long,tcan,largo,lamba,towil,dlini,' # tcanlartowdlam
    # createWord(inputLineEntry)
    # inputLineEntry = '+,example,lidza,ehemplo,udahran,mital,primer,'
    # createWord(inputLineEntry)
    # inputLineEntry = '0,get,hwod,konsegi,pa,istalama,dostava,'
    # createWord(inputLineEntry)
    print('\nCREATED WORD:')
    print(wordCreated)
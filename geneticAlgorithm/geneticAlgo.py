from random import randint
from operator import itemgetter
import ast # to convert string of list to actual list
import collections
import re

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
numGenerations = 500
epochMilestone = numGenerations//10
population = []
scoreHistory = []
scoreHistory2 = []
wordHistory = []

debugOn = False

count = 0
countNew = 0
scoreImprovements = 0

creatingFromScratch = True

if debugOn:
    import matplotlib.pyplot as plt

#------------------------
# functions:
#------------------------

def evaluateScore_LettersFromEachSource(word,originalWords):
    score = 0
    consonantsAlreadyUsed = []
    for letter in word:
        # avoid using the same letter again anywhere in the same word:
        if letter not in consonantsAlreadyUsed:
            consonantsAlreadyUsed.append(letter)
            # encourage using words with letters found in all source words:
            for srcWord in originalWords:
                score += 1 if letter in srcWord else 0
    return score


def getFirstSyllable(string):
    syll = re.search(r'[^aeiou]+[aeiou][^aeiou]?',string)
    if syll:
        return syll.group() # CV, CVC, CCVC, ...
    return string # in case word only has vowels (V or VV...)


def respellWithAllophones(word):
    for char in word:
        for allo in allophones:
            if char in allo:
                word = word.replace(char,allophones[allo])
    return word


def evaluateScore_UsesFirstSyllablesAllophones(newWord, originalWords):
    score = 0
    srcSyllables = [getFirstSyllable(srcWord) for srcWord in originalWords if srcWord!=None]
    for syllable in srcSyllables:
        if respellWithAllophones(syllable) in respellWithAllophones(newWord):
            score += len(syllable)*2 # *2 to make it more worth it
    return score


def penalizeConsonantClusters(word):
    score = 0
    consonantClusterLength = 0
    for letter in word:
        if letter not in 'aeiou':
            consonantClusterLength += 1
        else:
            if consonantClusterLength > 1:
                score -= consonantClusterLength
            consonantClusterLength = 0
    # in case the word ends with a consonant:
    score -= consonantClusterLength
    return score


def penalizeLength(newWord):
    return -len(newWord)


def evaluate(line):
    newWord = line.split(',')[0]
    originalWords = line.split(',')[2:]
    score = 0
    # encourage using letters from ALL src words, but avoid repeating letters like in "mmmmmmommmmmmm":
    score += evaluateScore_LettersFromEachSource(newWord, originalWords)
    score += evaluateScore_UsesFirstSyllablesAllophones(newWord,originalWords)
    # avoid consonant clusters like in "htkyowaz" or "kdyspgunwa"
    score += penalizeConsonantClusters(newWord)
    score += penalizeLength(newWord)
    return score


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


def constructWord(sourceWords, instructions):
    newWord = []
    i = 0
    lang = 0
    wordIndices = [0] * len(sourceWords)
    for instruction in instructions:
        if instruction == 'x':
            break
        elif instruction == '+':
            # make '+' per language, so don't lose out on initial letters in different words
            wordIndices[lang] += 1
        else: # instruction = lang 0,1,2,3,4
            lang = instruction
            sourceWord = sourceWords[lang]
            i = wordIndices[lang]
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
    secondBestScore = population[2][0]
    scoreHistory.append(currentBestScore)
    scoreHistory2.append(secondBestScore)


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
    return int(str(entry).split(', ',1)[0][1:]) # [1:] to remove initial '['


def printDebug(*args):
    if debugOn:
        print(' '.join([str(arg) for arg in args]))

#------------------------
# main part of the program:
#------------------------

def createWord(inputLineEntry):
    global population
    global scoreHistory
    global scoreHistory2
    global wordHistory
    global count
    global countNew
    global scoreImprovements
    global creatingFromScratch
    
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
    scoreHistory2 = []
    wordHistory = []
    
    # initialize population
    for i in range(popSize):
        instructions = generateNewIndividual()
        newWord = constructWord(srcWords, instructions)
        entry = newWord + ',' + engWord + ',' + ','.join(srcWords) + ',' # should have 7 commas
        score = evaluate(entry)
        individual = [score, entry, instructions]
        population.append(individual)
    
    # randomize whether initialization includes previous best-scorer in this session's population
    # (later will still compare to it anyways to check for improved score)
    cointoss = randint(0,1)
    if cointoss == 0:
        creatingFromScratch = True
    elif cointoss == 1:
        # make use of preexisting best-scorer saved externally
        scorersFile = 'best-scorers.txt'
        scorers = []
        creatingFromScratch = False
        with open(scorersFile,'r') as f:
            scorers = f.read().splitlines()
        if scorers != []:
            for scorer in scorers:
                prevScorer_id = getEntryIdentifier(scorer)
                if prevScorer_id == getEntryIdentifier(population[0]):
                    prevBestScore = int(float(scorer.split(', ')[0].replace('[','')))
                    prevBestEntry = scorer.split(', ')[1].replace('\'','')
                    prevBestInstruction = ast.literal_eval(scorer.split(', ',2)[2][:-1]) # [:-1] to remove final ']'
                    prevBest = [prevBestScore,prevBestEntry,prevBestInstruction]
                    # include preexisting best-scorer saved externally
                    population.append(prevBest)
    
    # starting "from scratch"? allow more generations before comparing with best scorer
    adjustForFromScratch = 1
    if creatingFromScratch:
        adjustForFromScratch = 2
    
    # train
    for i in range(numGenerations * adjustForFromScratch):
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
            newWord = constructWord(srcWords, instructions)
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
            if len(instructions_toMutate) == 0:
                instructions_toMutate = ''
            else:
                for mutation in range(3):
                    # mutate instructions (replace/add/delete) at index_toMutate:
                    decide1replace2add3delete = randint(1,3)
                    index_toMutate = randint(0,len(instructions_toMutate)) # not -1 so that can add at end
                    atEnd = index_toMutate == len(instructions_toMutate)
                    if decide1replace2add3delete == 1 and instructions_toMutate:
                        if atEnd: # check if 1 out of range
                            index_toMutate -= 1
                        # replace instruction at index_toMutate
                        instruction_toReplace = possibleInstructions[ randint(0,len(possibleInstructions)-1) ]
                        instructions_toMutate[index_toMutate] = instruction_toReplace
                    elif decide1replace2add3delete == 2:
                        # add instruction at index_toMutate
                        instruction_toAdd = possibleInstructions[ randint(0,len(possibleInstructions)-1) ]
                        instructions_toMutate.insert(index_toMutate, instruction_toAdd)
                    elif decide1replace2add3delete == 3 and instructions_toMutate:
                        if atEnd: # check if 1 out of range
                            index_toMutate -= 1
                        # delete instruction at index_toMutate
                        del instructions_toMutate[index_toMutate]
            instructions = instructions_toMutate
            newWord = constructWord(srcWords, instructions)
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
    newWord = constructWord(srcWords, instructionsBestSoFar)
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
    
    # save best scorer externally
    scorersFile = 'best-scorers.txt'
    scorers = []
    with open(scorersFile,'r') as f:
        scorers = f.read().splitlines()
    if scorers == []:
        # just initialize file if nothing there
        with open(scorersFile,'w') as f:
            f.write(str(bestSoFar)+'\n')
        bestSoFar_word = entryBestSoFar.split(',')[0].replace('\'','')
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
            countNew += 1
            print('NEW WORDS:',countNew)
        else:
            # check each line
            for scorer in scorers:
                prevScorer_id = getEntryIdentifier(scorer)
                if prevScorer_id == bestSoFar_id:
                    prevScorer_scr = getEntryScore(scorer)
                    prevScorer_word = scorer.split(',')[1].replace(' \'','')
                    # include only better scorer
                    if bestSoFar_scr > prevScorer_scr:
                        newScorers.append(bestSoFar)
                        print(prevScorer_word + ' -> ')
                        print(bestSoFar)
                        countNew += 1
                        print('NEW WORDS:',countNew)
                        scoreImprovements += bestSoFar_scr - prevScorer_scr
                        print('SCORE IMPROVEMENT SUM:',scoreImprovements)
                    else:
                        newScorers.append(scorer)
                        # replace with previously existing scorer as output word
                        bestSoFar_word = prevScorer_word
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
    inputLineEntry = '0,use,yun,usa,istemal,istemal,potrebi,' # yunsastempot
    wordCreated = createWord(inputLineEntry)
    # inputLineEntry = '0,be,ca,esta,ho,kana,bi,' # castahokanbi
    # wordCreated = createWord(inputLineEntry)
    print('\nCREATED WORD:')
    print(wordCreated)
    if debugOn:
        title = 'Score History'
        # plot score over generations:
        plt.plot(scoreHistory)
        # show second-bests if external scorer was put in population
        if not creatingFromScratch:
            title += ' - USING PREVIOUS BEST SCORER'
            plt.plot(scoreHistory2)
        plt.title(title)
        plt.show()
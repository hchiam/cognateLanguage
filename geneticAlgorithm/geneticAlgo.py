from random import randint
from operator import itemgetter
import ast # to convert string of list to actual list
import collections

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
numGenerations = 250
epochMilestone = numGenerations//10
population = []
scoreHistory = []
scoreHistory2 = []
wordHistory = []

debugOn = True

count = 0

creatingFromScratch = True

if debugOn:
    import matplotlib.pyplot as plt

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
    consonantsAlreadyUsed = []
    for letter in word:
        # avoid using the same letter again anywhere in the same word:
        if letter not in consonantsAlreadyUsed:
            consonantsAlreadyUsed.append(letter)
            # encourage using words with letters found in all source words:
            for srcWord in originalWords:
                score += 1 if letter in srcWord else 0
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


def evaluate(line):
    newWord = line.split(',')[0]
    originalWords = line.split(',')[2:]
    score = 0
    
    # evaluators with different weighting priorities for different source languages:
    score += evaluateScore_AlloWithVowels(newWord, originalWords)
    score += evaluateScore_ConsonantsInOrder(newWord, originalWords)
    
    # encourage using letters from ALL src words, but avoid repeating letters like in "mmmmmmommmmmmm":
    score += evaluateScore_LettersFromEachSource(newWord, originalWords)
    
    # avoid consonant clusters like in "htkyowaz" or "kdyspgunwa"
    score += penalizeConsonantClusters(newWord)
    
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
    return str(entry).split(', ',1)[0][1:] # [1:] to remove initial '['


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
                    prevBestScore = float(scorer.split(', ')[0].replace('[',''))
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
            if len(instructions_toMutate) > 0:
                for i in range(3):
                    # mutate instructions
                    index_toMutate = randint(0,len(instructions_toMutate))
                    # TODO: make "add instruction" a coin toss and be able to insert at any index
                    # TODO: add "delete instruction", so then a 3-way coin toss of sorts
                    if index_toMutate == len(instructions_toMutate):
                        # add instruction
                        instruction_toAdd = possibleInstructions[ randint(0,len(possibleInstructions)-1) ]
                        if instruction_toAdd != 'x':
                            instructions_toMutate.append(instruction_toAdd)
                    else:
                        # modify instruction
                        instruction_toReplace = possibleInstructions[ randint(0,len(possibleInstructions)-1) ]
                        if instruction_toReplace != 'x':
                            instructions_toMutate[index_toMutate] = instruction_toReplace
                        else:
                            instructions_toMutate = instructions_toMutate[index_toMutate-1:]
            else:
                instructions_toMutate = ''
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
    # inputLineEntry = '+,i,wo,yo,me,ana,ya,' # should NOT be missing English word like this: '[94.5, 'y,wo,yo,me,ana,ya,', [4]]'
    # wordCreated = createWord(inputLineEntry)
    # inputLineEntry = '+,to,daw,a,ko,le,na,' # this one used to output ''
    # wordCreated = createWord(inputLineEntry)
    # inputLineEntry = '+,make,djidzaw,ase,bana,sana,dela,' # this one used to output 'abaaaaaasanlaaaaaaadaa'
    # wordCreated = createWord(inputLineEntry)
    inputLineEntry = '0,use,yun,usa,istemal,istemal,potrebi,' # yunsastempot
    wordCreated = createWord(inputLineEntry)
    # inputLineEntry = '+,long,tcan,largo,lamba,towil,dlini,' # tcanlartowdlam
    # wordCreated = createWord(inputLineEntry)
    # inputLineEntry = '+,example,lidza,ehemplo,udahran,mital,primer,'
    # wordCreated = createWord(inputLineEntry)
    # inputLineEntry = '0,get,hwod,konsegi,pa,istalama,dostava,'
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
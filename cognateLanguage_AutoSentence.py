# automatically generates sentences based on source words
# from output_shortlist.txt
# with a=action (verb), d=descriptor (adjective/adverb), t=thing (noun/pronoun), c=connector (preposition)

import random

filename1 = 'output_shortlist.txt'

# get lines of file into a list:
with open(filename1,'r') as f1:
    data = f1.readlines()

def justTwoInitSylls(word):
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

def countVowels(word):
    vowels = 'aeiou'
    word = word.lower()
    count = 0
    for char in word:
        if char in vowels:
            count += 1
    return count

def getWord(wordType='d',fullWords=True):
    global data # needed to access data without constantly re-getting data first
    
    if wordType!='c':
        i = random.randrange(0,len(data))
        label = data[i].split(',')[-1].strip() # need .strip() to remove whitespace character(s)
        while label != wordType:
            i = random.randrange(0,len(data))
            label = data[i].split(',')[-1].strip() # need .strip() to remove whitespace character(s)
        word = data[i].split(',')[0]
        translation = data[i].split(',')[1]
    elif wordType=='c':
        connectorIndices = [7,8,231,232,233,234,235,236,237,238,239,240,241,242,243,312,369,370,371,377,421]
        i = random.choice(connectorIndices)
        word = data[i].split(',')[0]
        translation = data[i].split(',')[1]

    if fullWords==False:
        word = justTwoInitSylls(word)
    
    return word, translation

def buildSentence(pattern,fullWords=True):
    sentence = ''
    translation = ''
    trackLastLetterOfLastWord = ''
    for letter in pattern:
        newword, newwordtrans = getWord(wordType=letter,fullWords=fullWords)
        if fullWords:
            sentence += newword + ' '
        else: # if short word translation:
            trackLastLetterOfLastWord = newword[-1]
            numVowelsInTranslatedWord = countVowels(newword)
            if numVowelsInTranslatedWord == 1:
                sentence += newword
                trackLastLetterOfLastWord = ''
            elif trackLastLetterOfLastWord in 'aeiou':
                sentence += newword
            else:
                sentence += newword[:-1]
        translation += newwordtrans + ' '
    # remove last space, capitalize first letter, add period at end:
    if fullWords:
        sentence, translation = sentence.rstrip().capitalize()+'.', translation.rstrip().capitalize()+'.'
    else:
        sentence, translation = sentence.rstrip()+trackLastLetterOfLastWord, translation.rstrip().capitalize()+'.'
    return sentence, translation




# if this .py file is being run as a standalone by the user:
if __name__ == '__main__':
    print('')
    print('WARNING: Words are chosen at random within word types and may produce unexpected sentences.')
    print('')
    
    pattern = 'tat'
    print('AUTO-GENERATED SENTENCE 1: ***1***, with pattern "'+pattern+'":')
    sentence, translation = buildSentence(pattern,False)
    print(sentence)
    print(translation)
    
    print('')
    
    pattern = 'tact'
    print('AUTO-GENERATED SENTENCE 2: ***2***, with pattern "'+pattern+'":')
    sentence, translation = buildSentence(pattern,False)
    print(sentence)
    print(translation)
    
    print('')
    
    pattern = 'dtadtcdt'
    print('AUTO-GENERATED SENTENCE 3: ***3***, with pattern "'+pattern+'":')
    sentence, translation = buildSentence(pattern,False)
    print(sentence)
    print(translation)
    
    print('')
    
    pattern = 'tat'
    print('AUTO-GENERATED SENTENCE 4: ***1***, with pattern "'+pattern+'" and full words:')
    sentence, translation = buildSentence(pattern,True)
    print(sentence)
    print(translation)
    
    print('')
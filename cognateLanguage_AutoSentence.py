# automatically generates sentences based on source words
# from output_shortlist.txt
# with a=action (verb), d=descriptor (adjective/adverb), t=thing (noun/pronoun), c=connector (preposition)

import random

filename1 = 'output_shortlist.txt'

# get lines of file into a list:
with open(filename1,'r') as f1:
    data = f1.readlines()

def getWord(wordType='d'):
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
        connectorIndices = [7,8,231,232,233,234,235,236]
        i = random.choice(connectorIndices)
        word = data[i].split(',')[0]
        translation = data[i].split(',')[1]
    
    return word, translation

def buildSentence(pattern):
    sentence = ''
    translation = ''
    for letter in pattern:
        newword, newwordtrans = getWord(wordType=letter)
        sentence += newword + ' '
        translation += newwordtrans + ' '
    # remove last space, capitalize first letter, add period at end:
    sentence, translation = sentence.rstrip().capitalize()+'.', translation.rstrip().capitalize()+'.'
    return sentence, translation




# if this .py file is being run as a standalone by the user:
if __name__ == '__main__':
    print('')
    
    pattern = 'tat'
    print('AUTO-GENERATED SENTENCE 1: ***1***, with pattern "'+pattern+'"')
    sentence, translation = buildSentence(pattern)
    print(sentence)
    print(translation)
    
    print('')
    
    pattern = 'tact'
    print('AUTO-GENERATED SENTENCE 2: ***2***, with pattern "'+pattern+'"')
    sentence, translation = buildSentence(pattern)
    print(sentence)
    print(translation)
    
    print('')
    
    pattern = 'dtadtcdt'
    print('AUTO-GENERATED SENTENCE 3: ***3***, with pattern "'+pattern+'"')
    sentence, translation = buildSentence(pattern)
    print(sentence)
    print(translation)
    
    print('')
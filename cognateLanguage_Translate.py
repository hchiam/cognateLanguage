import string # example use here:  to be able to remove punctuation
import re # example use here:  to be able to remove repeating spaces

from dictAsFile_wrapper import *

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

def indexOfNthInstanceOfVowel(mystr,n):
    vowels = 'aeiou'
    count = 0
    for i,letter in enumerate(mystr):
        if letter in vowels:
            count += 1
            if count == n:
                return i
    return None # in case cannot find

def vowelGroupCount(myStr):
    vowels = 'aeiou'
    count = 0
    for i,letter in enumerate(myStr):
        if i<len(myStr)-1 and myStr[i+1] == letter:
            continue
        if letter in vowels:
            count += 1
    return count

def isEven(num):
    return num%2 == 0

filename = 'hashtable.pkl' # 'output_shortlist.txt'
data = {}
input = ''
translation = '< Translation Not Found. >'

input = raw_input('Enter English word or sentence gloss to translate:\n\t')

# remove punctuation from input, except for '?'
exclude = set(string.punctuation)
input = ''.join(ch for ch in input if (ch not in exclude or ch == '?'))

# add space before '?' to enable replacing with question particle word
input = input.replace('?',' ?')

# make input all lowercase
input = input.lower()

# remove repeating spaces from what remains
input = re.sub(' +', ' ', input)

# print input # debug output

if input != "":
    
    translation = ''
    shortTranslation = ''
    trackLastLetterOfLastWord = ''
    
    # # get lines of file into a list
    # with open(filename,'r') as f:
    #     data = f.readlines()
    
    # get hashtable file into a dictionary
    data = readFileToDict(filename)
    
    # detect CogLang as input by checking if input is one abnormally long 'word' (and isn't found to be an English entry) and other indicators
    if (' ' not in input and input not in data and len(input) >= 9 and isEven(vowelGroupCount(input))):
        
        # split input into words by every 2nd vowel (and final consonant of sentence-word)
        newInput = []
        while len(input) > 1:
            nextIndex = indexOfNthInstanceOfVowel(input,2)
            if nextIndex != len(input)-2:
                newInput.append(input[:nextIndex+1])
            else:
                newInput.append(input)
            input = input[nextIndex+1:]
        
        # get .txt file file into a dictionary
        filename = 'output_shortlist.txt'
        with open(filename,'r') as f:
            data = f.readlines()
        data = [line.strip() for line in data]
        
        for word in newInput:
            
            translationFound = False
            
            # search list for reverse word translation to English
            for line in data:
                if line != '\n' and ',' in line:
                    if word == line[0:len(word)]:
                        translatedWord = line.split(',')[1]
                        if translatedWord != '?':
                            shortTranslatedWord = justTwoInitSylls(translatedWord)
                            numVowelsInTranslatedWord = countVowels(translatedWord)
                            translation += translatedWord + ' '
                        else:
                            translation = translation[:-1] + translatedWord + '?'
                        translationFound = True
            
            # add in '?' for words not found
            if translationFound == False:
                translation += '[?]' + ' '
        shortTranslation = "(N/A for English.)"
        
    else: # otherwise English sentence detected --> translate to Coglang
        
        # split input into words
        input = input.split(' ')
        
        for word in input:
            
            translationFound = False
            
            # # search for word translation in list
            
            # account for plural nouns or 2nd person singular verbs
            if word not in data and word[-1] == 's' and word[:-1] in data:
                word = word[:-1]
            
            # search for word translation in data ("data" is a hashtable/dictionary)
            if word in data:
                translatedWord = data[word]
                shortTranslatedWord = justTwoInitSylls(translatedWord)
                # trackLastLetterOfLastWord = shortTranslatedWord[-1] # THIS GOES WITH ADDING FINAL LETTER AT END OF SENTENCE
                numVowelsInTranslatedWord = countVowels(translatedWord)
                shortTranslation += ' ' + shortTranslatedWord
                # if numVowelsInTranslatedWord == 1:
                #     shortTranslation += translatedWord
                #     trackLastLetterOfLastWord = ''
                # elif trackLastLetterOfLastWord in 'aeiou':
                #     shortTranslation += shortTranslatedWord
                # else:
                #     # shortTranslation += shortTranslatedWord[:-1] # THIS GOES WITH ADDING FINAL LETTER AT END OF SENTENCE
                #     shortTranslation += shortTranslatedWord
                translation += translatedWord + ' '
                translationFound = True
                
            # add in '?' for words not found
            if translationFound == False:
                translation += '[?]' + ' '

# remove final space ' '
translation = translation[:-1]
# # add final letter
# shortTranslation += trackLastLetterOfLastWord # THIS GOES WITH REMOVING FINAL LETTER FROM EACH WORD

print 'Long Translation:\n\t' + '"' + translation.capitalize()+'.' + '"'
print 'Short Translation:\n\t' + shortTranslation
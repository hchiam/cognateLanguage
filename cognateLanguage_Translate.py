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
    # split input into words
    input = input.split(' ')
    
    translation = ''
    shortTranslation = ''
    trackLastLetterOfLastWord = ''
    
    # # get lines of file into a list
    # with open(filename,'r') as f:
    #     data = f.readlines()
    
    # get hashtable file into a dictionary
    data = readFileToDict(filename)
    
    for word in input:
        
        translationFound = False
        
        # # search for word translation in list
        
        # search for word translation in data ("data" is a hashtable/dictionary)
        if word in data:
            translatedWord = data[word]
            shortTranslatedWord = justTwoInitSylls(translatedWord)
            trackLastLetterOfLastWord = shortTranslatedWord[-1]
            numVowelsInTranslatedWord = countVowels(translatedWord)
            if numVowelsInTranslatedWord == 1:
                shortTranslation += translatedWord
                trackLastLetterOfLastWord = ''
            elif trackLastLetterOfLastWord in 'aeiou':
                shortTranslation += shortTranslatedWord
            else:
                shortTranslation += shortTranslatedWord[:-1]
            translation += translatedWord + ' '
            translationFound = True
            
        # add in '?' for words not found
        if translationFound == False:
            translation += '[?]' + ' '

    # remove final space ' '
    translation = translation[:-1]
    # add final letter
    shortTranslation += trackLastLetterOfLastWord

print 'Long Translation:\n\t' + '"' + translation.capitalize()+'.' + '"'
print 'Short Translation:\n\t' + shortTranslation
import string # example use here:  to be able to remove punctuation
import re # example use here:  to be able to remove repeating spaces

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

filename = 'output_shortlist.txt'
data = ''
input = ''
translation = '< Translation Not Found. >'

input = raw_input('Enter English word or sentence to translate:\n\t')

# remove punctuation from input
exclude = set(string.punctuation)
input = ''.join(ch for ch in input if ch not in exclude)

# make input all lowercase
input = input.lower()

# remove repeating spaces from what remains
input = re.sub(' +', ' ', input)

print input

if input != "":
    # split input into words
    input = input.split(' ')
    
    translation = ''
    shortTranslation = ''
    trackLastLetterOfLastWord = ''
    
    # get lines of file into a list
    with open(filename,'r') as f:
        data = f.readlines()
    
    for word in input:
        
        translationFound = False
        
        # search for word translation in list
        for line in data:
            if line != '\n' and ',' in line:
                if word == line.split(',')[1]:
                    translatedWord = line.split(',')[0]
                    shortTranslatedWord = justTwoInitSylls(translatedWord)
                    trackLastLetterOfLastWord = shortTranslatedWord[-1]
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

print 'Translation:\n\t' + translation.capitalize()+'.' + '"'
print 'Shortened:\n\t' + shortTranslation
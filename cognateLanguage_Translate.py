import string # example use here:  to be able to remove punctuation
import re # example use here:  to be able to remove repeating spaces

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
    
    for word in input:
        # get lines of file into a list
        with open(filename,'r') as f:
            data = f.readlines()
        
        translationFound = False
        
        # search for word translation in list
        for line in data:
            if word == line.split(',')[1]:
                translation += line.split(',')[0] + ' '
                translationFound = True
        
        # add in '?' for words not found
        if translationFound == False:
            translation += '[?]' + ' '

    # remove final space ' '
    translation = translation[:-1]

print 'Translation:\n\t', '"' + translation + '"'
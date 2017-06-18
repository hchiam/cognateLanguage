import sys
    
data = []

# use different import based on python version number:
if (sys.version_info > (3, 0)):
    # python 3:
    import urllib.request
    with urllib.request.urlopen('https://raw.githubusercontent.com/hchiam/cognateLanguage/master/output_shortlist.txt') as response:
        line = response.readline().decode('utf-8').replace('\n','')
        while line != '':
            data.append(line)
            line = response.readline().decode('utf-8').replace('\n','')
else: 
    # python 2:
    import urllib2
    response = urllib2.urlopen('https://raw.githubusercontent.com/hchiam/cognateLanguage/master/output_shortlist.txt')
    data = response.read().split('\n')

import string # example use here:  to be able to remove punctuation
import re # example use here:  to be able to remove repeating spaces

keepGoing = True

while keepGoing:
    
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
    
    # filename = 'output_shortlist.txt'
    # data = ''
    # input = ''
    translation = '< Translation Not Found. >'
    shortTranslation = '< Translation Not Found. >'
    
    if (sys.version_info > (3, 0)):
        inputData = input('Enter English word or sentence gloss to translate:\n\t')
    else:
        inputData = raw_input('Enter English word or sentence gloss to translate:\n\t')
    
    # remove punctuation from inputData, except for '?'
    exclude = set(string.punctuation)
    inputData = ''.join(ch for ch in inputData if (ch not in exclude or ch == '?'))
    
    # add space before '?' to enable replacing with question particle word
    inputData = inputData.replace('?',' ?')
    
    # make inputData all lowercase
    inputData = inputData.lower()
    
    # remove repeating spaces from what remains
    inputData = re.sub(' +', ' ', inputData)
    
    # print inputData # debug output
    
    if inputData != "":
        # split inputData into words
        inputData = inputData.split(' ')
        
        translation = ''
        shortTranslation = ''
        trackLastLetterOfLastWord = ''
        
        for word in inputData:
            
            translationFound = False
            
            # search for word translation in list
            for line in data:
                if line != '\n' and ',' in line:
                    if word == line.split(',')[1] or (word[-1] == 's' and word[:-1] == line.split(',')[1]): # (also account for plural nouns or 2nd person singular verbs)
                        translatedWord = line.split(',')[0]
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
    
    print ('Long Translation:\n\t' + '"' + translation.capitalize()+'.' + '"')
    print ('Short Translation:\n\t' + shortTranslation)
    
    if (sys.version_info > (3, 0)):
        userResponse = input('Another sentence? (y/n):\n\t').lower()
    else:
        userResponse = raw_input('Another sentence? (y/n):\n\t').lower()
    keepGoing = ('y' == userResponse) or ('yes' == userResponse)
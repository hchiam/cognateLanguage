def justTwoInitSylls_CVC(word):
    beforeThisIndex = 0
    afterThisIndex = 0
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

# get "shortform(word),English" pairs
filename = 'output_shortlist.txt'
entries = []
with open(filename,'r') as f:
    for line in f:
        # get just the output words
        word = line.split(',')[0].replace(' \'','')
        word = justTwoInitSylls_CVC(word)
        english = line.split(',')[1]
        entries.append(word+','+english+'\n')

# save pairs to a separate file
filename = 'shortforms.txt'
with open(filename,'w') as f:
    for entry in entries:
        f.write(entry)
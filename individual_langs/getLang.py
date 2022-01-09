data = []

inputFile = '../output_shortlist.txt' # '../' makes it look at the folder directory one above for that file
with open(inputFile,'r') as f1:
    data = f1.readlines()

langs = ['Chi','Spa','Hin','Ara','Rus']
for i,lang in enumerate(langs):
    outputFile = 'just' + lang + '.txt'
    with open(outputFile,'a') as f2:
        f2.truncate(0)
        for line in data:
            entry = line.split(',')
            f2.write(entry[i+2] + ',' + entry[1] + ' (' + lang + ')' + '\n') # i+2 because item 0=CogLang and 1=Eng
data = []

inputFile = '../output.txt' # '../' makes it look at the folder directory one above for that file
with open(inputFile,'r') as f1:
    data = f1.readlines()

langs = ['Mal','Kor','Swa','Japa']
for i,lang in enumerate(langs):
    outputFile = 'just' + lang + '.txt'
    for line in data:
        if ',' in line:
            entry = line.split(',')
            with open(outputFile,'a') as f2:
                f2.write(entry[i+2] + ',' + entry[1] + ' (' + lang + ')' + '\n') # i+2 because item 0=MalKorSwaJapa and 1=Eng
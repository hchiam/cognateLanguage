data = []

inputFile = '../output.txt' # '../' makes it look at the folder directory one above for that file
with open(inputFile,'r') as f1:
    data = f1.readlines()

outputFile = 'for_memrise.txt'
for line in data:
    if ',' in line:
        entry = '\t'.join(line.split(',')[:2]) + '\n' # 2 because item 0=word and 1=Eng
        with open(outputFile,'a') as f2:
            f2.write(entry)
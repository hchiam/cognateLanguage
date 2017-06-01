from collections import Counter

scorersFile = 'best-scorers.txt'
scorers = []
with open(scorersFile,'r') as f:
    for line in f:
        # get just the words
        scorers.append(line.split(',')[1].replace(' \'',''))

collisions = [k for k,v in Counter(scorers).items() if v>1]
print(len(collisions),'word collisions:\n',collisions)

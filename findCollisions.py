from collections import Counter

def countCollisions(entries):
    collisions = [k for k,v in Counter(entries).items() if v>1]
    num_collisions = len(collisions)
    print(num_collisions,'word collisions:\n',collisions)
    return num_collisions

def countCollisionsInFile(filename):
    entries = []
    with open(filename,'r') as f:
        for line in f:
            # get just the words
            entries.append(line.split(',')[1].replace(' \'',''))
    return countCollisions(entries)

def countCollisionsInList(entries):
    return countCollisions(entries)

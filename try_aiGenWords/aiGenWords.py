from evalWord import *

input_file = 'data.txt'
output_file = 'output.txt'
data = []

def getData():
    with open(input_file,'r') as f:
        data = f.readlines()
    return data

def compareScoreW2MinusW1(word1,word2):
    res1 = evaluateLine(word1)
    res2 = evaluateLine(word2)
    comparisons = [round(res2[i]-res1[i],1) for i in range(len(res1))]
    # print res1, res2
    return comparisons
    # return evaluateLine(word2)-evaluateLine(word1)

data = getData()
print(data[10])
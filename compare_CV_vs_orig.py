from evalWord import *

filename1 = 'output_shortlist.txt'
filename2 = 'output_CV_srcSylls.txt'
filename3 = 'result_compare_CV_vs_orig.txt'
data_f1 = []
data_f2 = []

def compareScoreW2MinusW1(word1,word2):
    res1 = evaluateLine(word1)
    res2 = evaluateLine(word2)
    comparisons = [round(res2[i]-res1[i],1) for i in range(len(res1))]
    # print res1, res2
    return comparisons
    # return evaluateLine(word2)-evaluateLine(word1)

def getData():
    global data_f1 # needed to modify variable outside of function
    global data_f2 # needed to modify variable outside of function
    with open(filename1,'r') as f1:
        data_f1 = f1.readlines()
    
    with open(filename2,'r') as f2:
        data_f2 = f2.readlines()

def writeAllComparisons():
    score = 0
    getData()
    for i in range(len(data_f1)):
        line_f1 = data_f1[i]
        line_f2 = data_f2[i]
        result = compareScoreW2MinusW1(line_f1,line_f2)
        word_f1 = data_f1[i].split(',')[0]
        word_f2 = data_f2[i].split(',')[0]
        msg = ''
        if result[0] > 0 and result[1] > 0 and result[3] < 0:
            msg = ' USE THE CV VERSION!!! ' + line_f2.split(',', 1)[1][:-1]
            score += 1
        with open(filename3,'a') as f3:
            f3.write(str(result) + ' \t' + word_f2 + ' vs ' + word_f1 + msg + '\n')
    with open(filename3,'a') as f3:
        f3.write('SCORE: ' + str(score) + ' out of ' + str(len(data_f1)) + ' = ' + str(round(score*1.0/len(data_f1)*100,2)) + '%')

def writeBetterComparisons():
    score = 0
    getData()
    for i in range(len(data_f1)):
        line_f1 = data_f1[i]
        line_f2 = data_f2[i]
        result = compareScoreW2MinusW1(line_f1,line_f2)
        word_f1 = data_f1[i].split(',')[0]
        word_f2 = data_f2[i].split(',')[0]
        msg = ''
        if result[0] > 0 and result[1] > 0 and result[3] < 0:
            msg = 'CV  \t' + word_f2 + ' ' + line_f2.split(',', 1)[1][:-1] + ' ' + str(result) + ' vs ' + word_f1
            score += 1
        else:
            msg = 'orig\t' + word_f1 + ' ' + line_f2.split(',', 1)[1][:-1]
        with open(filename3,'a') as f3:
            f3.write(msg + '\n')
    with open(filename3,'a') as f3:
        f3.write('SCORE: ' + str(score) + ' out of ' + str(len(data_f1)) + ' = ' + str(round(score*1.0/len(data_f1)*100,2)) + '%')



# writeAllComparisons()
writeBetterComparisons()

import sys

from dictAsFile_wrapper import *

def run():
    hashtableName = 'hashtable.pkl'
    data = {}
    
    # use different import based on python version number:
    if (sys.version_info > (3, 0)):
        # python 3:
        print('python 3')
        import urllib.request
        url = 'https://raw.githubusercontent.com/hchiam/cognateLanguage/master/hashtable.pkl'
        urllib.request.urlretrieve(url) # download file
        data = readFileToDict(hashtableName)
        # with urllib.request.urlopen('https://raw.githubusercontent.com/hchiam/cognateLanguage/master/output_shortlist.txt') as response:
        #     line = response.readline().decode('utf-8').replace('\n','')
        #     while line != '':
        #         data.append(line)
        #         line = response.readline().decode('utf-8').replace('\n','')
    else: 
        # python 2:
        print('python 2')
        import urllib2
        url = 'https://raw.githubusercontent.com/hchiam/cognateLanguage/master/hashtable.pkl'
        response = urllib2.urlopen(url) # download file
        data = readFileToDict(hashtableName)
        # response = urllib2.urlopen('https://raw.githubusercontent.com/hchiam/cognateLanguage/master/output_shortlist.txt')
        # data = response.read().split('\n')
    return data

# this if statement is so that the following code only runs if this .py file is not being imported
if __name__ == '__main__':
    data = run()
    # debug print out:
    print ('debug output: data[\"hi\"] = ' + data["hi"])
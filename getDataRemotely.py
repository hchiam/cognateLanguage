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

# debug print out:
print ('test: data[0] = ' + data[0])
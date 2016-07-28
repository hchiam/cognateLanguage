filename = 'data.txt'

# get each line of file printed one by one:
#with open(filename,'r') as fh:
#    line = fh.readline()
#    while line:
#        print(line)
#        line = fh.readline()

# get lines of file into a list:
with open(filename,'r') as fh:
    data = fh.readlines()
#    print data

# initialize arrays:
words = {'English' : '', 'Chinese' : '', 'Arabic' : '', 'Spanish' : '', 'Hindi' : '', 'Russian' : ''}

# fill arrays:
for line in data:
    words['English'] = line.split(',')[1]
    words['Chinese'] = line.split(',')[2]
    words['Arabic'] = line.split(',')[3]
    words['Spanish'] = line.split(',')[4]
    words['Hindi'] = line.split(',')[5]
    words['Russian'] = line.split(',')[6]
    if words['English'] != 'English':
        break # get rid of this later

print words
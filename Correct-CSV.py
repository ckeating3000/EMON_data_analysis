#Correct-CSV.py
'''
03/07/2017
Sam Emery
'''

#Handle Imports
import os
import csv

#
#
#Define useful functions
#
#
'''Function to determine file type'''
def get_file_type(f):
    l = len(f)
    t = []
    for i in range(l-3,l):
        t.append(f[i])
    ts = ''.join(t)
    return ts
    del ts, t, l
'''Function to get the file name'''
def get_file_name(name):
    l = len(name)
    new_name = []
    for i in range(l-4):
        new_name.append(name[i])
    s = ''.join(new_name)
    return s
    del l,new_name,s

#
#
#Begin Script
#
#
#

#path = ('/home/sbemery/Desktop/GRE-Data/1_2017_EMON_Data')
path = ('/Users/Colin/Documents/Colin/College/Green Rehab Project/Python emon parsing/testing')

print path

files = os.listdir(path)
for fi in files:
	if get_file_type(fi) == 'CSV':
		print fi
		name = get_file_name(fi)
		print name
		f0 = open(path+'/'+fi,'rb')
		data = f0.read()
		f0.close()
		ff = open(path+'/'+name+'_fix.csv','wb')
		ff.write(data.replace('\x00',''))
		ff.close()

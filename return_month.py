#parse the master spreadsheet and return a month's worth of data, in summarized format
import sys, re, csv, codecs, os
from os import listdir
from os.path import isfile, join


# check for correct num args
if len(sys.argv)<3:
	sys.exit ("Usage: Python get_month_summary.py [numerical month] [master_spreadsheet_filename]")


#parameters needed (per building):
#Averages: 
#	   	total unit, lights, kitchen, laundry, HVAC, outlets, microwave, water heating 
#Unit: 
#		total unit, lights, kitchen, laundry, HVAC, outlets, microwave, water heating 

month = sys.argv[1]
print "month: " + month
full_month = []

with open(master_name, 'rb') as myfile: # open master file for reading and writing
    for line in myfile:
        temp_data = [datapt.date_time, datapt.building, datapt.unit, datapt.energy_use, datapt.monitor_type]
        for line in myfile:
        	for datapoint in line:
        		print datapoint

print "DONE"
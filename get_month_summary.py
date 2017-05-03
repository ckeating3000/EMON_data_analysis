#Author: Colin Keating
#4/14/17
#Intended for use with sql_csv_parse_5 script
#parse the master spreadsheet and return a month's worth of data, in summarized format
#   IMPORTANT: must save the master file as: Windows Comma Separated Values type
import sys, re, csv, codecs, os
from os import listdir
from os.path import isfile, join
import numpy as np


# check for correct num args
if len(sys.argv)!=3:
	sys.exit ("Usage: Python get_month_summary.py [mm-yy] [master_spreadsheet_filename]")

#parameters needed (per building):
#Averages: 
#	   	total unit, lights, kitchen, laundry, HVAC, outlets, microwave, water heating 
#Unit: 
#		total unit, lights, kitchen, laundry, HVAC, outlets, microwave, water heating 
date = sys.argv[1]
if len(date)!=5:
	sys.exit ("Usage: Python get_month_summary.py [mm-yy] [master_spreadsheet_filename]")
month = int(date.split("-")[0])
year = int(date.split("-")[1])

master_name = sys.argv[2]
print "month: " + str(month)
print "year: " + str(year)
print "file name: " + master_name
full_month = []

#   IMPORTANT: must save the master file as: Windows Comma Separated Values type

with open(master_name, 'rb') as myfile: # open master file for reading and writing
    #reader = csv.reader(myfile, dialect=csv.excel_tab) #, delimiter=' ', quotechar='|'
    reader = csv.reader(myfile, delimiter=',') #, delimiter=' ', quotechar='|'
    for line in reader:
    	#get the month and year from that line
    	date_time = line[0]
    	temp_month = int(date_time.split("/")[0])
    	temp_year = date_time.split("/")[2]
    	temp_year = int(temp_year.split(" ")[0])
    	print "temp month: " + str(temp_month)
    	print "temp_year : " + str(temp_year)
    	if (temp_year==year and temp_month==month):
    		full_month.append(line)

# 
Buildings  = {'745', '749'}
Units      = {'1N', '1S' ,'2N','2S','3N','3S'}
Subsystems = {'HVAC','Kitchen','Laundry','Washer','Dryer','Lights','GenRec','Microwave_N','Microwave_S','MakeupAir_N','MakeupAir_S','Water_Heater_N','Water_Heater_S','Spare'}

subsystem_totals = np.zeros((2,6,14))

for line in full_month:
	for b_index,b_value in enumerate(Buildings):
		for u_index, u_value in enumerate(Units):
			for s_index,s_value in enumerate(Subsystems):
				print 's_index: ' + str(s_index) + ' s_value: ' + str(s_value)
				if line[1]==b_value and line[2]==u_value and line[4]==s_value:
					subsystem_totals[b_index,u_index,s_index]=subsystem_totals[b_index,u_index,s_index]+float(line[3])

print subsystem_totals
'''
enumerate order:
749, 745
1S, 2S, 3S, 3N, 2N, 1N

s_index: 0 s_value: Water_Heater_S
s_index: 1 s_value: Laundry
s_index: 2 s_value: HVAC
s_index: 3 s_value: Microwave_S
s_index: 4 s_value: MakeupAir_N
s_index: 5 s_value: Lights
s_index: 6 s_value: GenRec
s_index: 7 s_value: Dryer
s_index: 8 s_value: Spare
s_index: 9 s_value: MakeupAir_S
s_index: 10 s_value: Microwave_N
s_index: 11 s_value: Washer
s_index: 12 s_value: Water_Heater_N
s_index: 13 s_value: Kitchen
'''

#month totals
# total_745=0.0
# total_749=0.0
# for line in full_month:
# 	if line[1] == "745":
# 		total_745 = total_745+float(line[3])
# 	elif line[1] == "749":
# 		total_749 = total_749+float(line[3])

# print "total 745:" + str(total_745)
# print "total_749:" + str(total_749)

# save output to CSV
with file(str(date) + '_report.csv', 'w') as outfile:
	# from http://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
    # Iterating through a ndimensional array produces slices along
    # the last axis. This is equivalent to data[i,:,:] in this case
    for data_slice in subsystem_totals:
        # The formatting string indicates that I'm writing out
        # the values in left-justified columns 7 characters in width
        # with 2 decimal places.  
        np.savetxt(outfile, data_slice, fmt='%-7.2f')
        # Writing out a break to indicate different slices...
        outfile.write('\n')

# output = np.asarray(subsystem_totals)
# np.savetxt("_report.csv", output, delimiter=",")

print "DONE"











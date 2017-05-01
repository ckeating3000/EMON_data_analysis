#Author: Colin Keating
#4/14/17
#Intended for use with sql_csv_parse_5 script
#parse the master spreadsheet and return a month's worth of data, in summarized format
#   IMPORTANT: must save the master file as: Windows Comma Separated Values type
import sys, re, csv, codecs, os
from os import listdir
from os.path import isfile, join


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

total_745=0.0
total_749=0.0
for line in full_month:
	if(line[1]) == "745":
		total_745 = total_745+float(line[3])

print total_745
print total_749

print "DONE"
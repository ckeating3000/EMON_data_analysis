import sys, re, csv

#check for correct num args
if len(sys.argv)<2:
	sys.exit ("Usage: python sql_csv_parse.py [filename]")
	
filename=sys.argv[1]

class DataPoint:
	def __init__(self, date_time, unit, energy_use, monitor_type):
		self.date_time = date_time
		self.unit = unit
		self.energy_use = energy_use
		self.monitor_type = monitor_type
	def __str__(self):
		return (self.date_time + " " +  self.unit + " " + self.energy_use + " " + self.monitor_type)

with open(filename, 'rU') as f:
    reader = csv.reader(f)
    reachdata = False
    
    unit_list = []
    monitor_type_list = []
    full_list = []
    for row in reader:
    	if not reachdata:
    		if row[0]=="start_here":
    			unit_list = row
    		if row[0] == "Date_Time":
    			monitor_type_list = row
    			reachdata = True
    	else:
    		for index, value in enumerate(row):
    			if index is not 0:
    				full_list.append(DataPoint(row[0], unit_list[index], value, monitor_type_list[index]))

    #for datapt in full_list:
    #	print (datapt)

    # push into csv
    # from http://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
with open('output.csv', 'wb') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for datapt in full_list:
	    wr.writerow([datapt.date_time, datapt.unit, datapt.energy_use, datapt.monitor_type,])

    # use sqlalchemy










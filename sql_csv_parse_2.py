#updated for use with the raw csv files received from Matt Stuart at Quadrangle Housing
import sys, re, csv, codecs

#check for correct num args
if len(sys.argv)<2:
	sys.exit ("Usage: python sql_csv_parse_2.py [filename]")
	
filename=sys.argv[1]

class DataPoint:
	def __init__(self, date_time, unit, energy_use, monitor_type):
		self.date_time = date_time
		self.unit = unit
		self.energy_use = energy_use
		self.monitor_type = monitor_type
	def __str__(self):
		return (self.date_time + " " +  self.unit + " " + self.energy_use + " " + self.monitor_type)
#For 749
#TODO: redo for both buildings
#create dictionary between meter code and unit number for 749                                                                                                                                                                                                                        # begin 1B                  
MeterID_to_Unit_749 = {'G2L1-1A1':'1S' , 'G2L1-1A2':'1S' , 'G2L1-1A3':'1N' , 'G2L1-1A4':'1N' , 'G2L1-1A5':'1N' , 'G2L1-1A6':'2N' , 'G2L1-1A7':'2N' , 'G2L1-1A8':'2N' , 
                       'G2L1-1B1':'1S' , 'G2L1-1B2':'1S' , 'G2L1-1B3':'2S' , 'G2L1-1B4':'2S' , 'G2L1-1B5':'2S' , 'G2L1-1B6':'2S' , 'G2L1-1B7':'2N' , 'G2L1-1B8':'2N' ,
                       'G2L2-2A1':'3N' , 'G2L2-2A2':'3N' , 'G2L2-2A3':'3N' , 'G2L2-2A4':'2S' , 'G2L2-2A5':'3S' , 'G2L2-2A6':'3S' , 'G2L2-2A7':'3S' , 'G2L2-2A8':'3S' ,
                       'G2L3-3A1':'1S' , 'G2L3-3A2':'1S' , 'G2L3-3A3':'1N' , 'G2L3-3A4':'1N' , 'G2L3-3A5':'2S' , 'G2L3-3A6':'2S' , 'G2L3-3A7':'2N' , 'G2L3-3A8':'2N' ,
                       'G2L3-3B1':'3S' , 'G2L3-3B2':'3S' , 'G2L3-3B3':'3N' , 'G2L3-3B4':'3N' , 'G2L3-3B5':'N'  , 'G2L3-3B6':'N'  , 'G2L3-3B7':'S'  , 'G2L3-3B8':'S'  ,
                    }
#create second dictionary between meter code and subsystem for 749
MeterID_to_Subsys_749 ={'G2L1-1A1':'GenRec'  , 'G2L1-1A2':'Spare'  , 'G2L1-1A3':'Kitchen' , 'G2L1-1A4':'Lights' , 'G2L1-1A5':'GenRec'    , 'G2L1-1A6':'Lights'    , 'G2L1-1A7':'GenRec'    , 'G2L1-1A8':'Spare1'    , 
                        'G2L1-1B1':'Kitchen' , 'G2L1-1B2':'Lights' , 'G2L1-1B3':'Kitchen' , 'G2L1-1B4':'Lights' , 'G2L1-1B5':'GenRec'    , 'G2L1-1B6':'Spare1'    , 'G2L1-1B7':'Kitchen'   , 'G2L1-1B8':'Spare2'    ,
                        'G2L2-2A1':'Kitchen' , 'G2L2-2A2':'Lights' , 'G2L2-2A3':'GenRec'  , 'G2L2-2A4':'Spare2' , 'G2L2-2A5':'Spare'     , 'G2L2-2A6':'Kitchen'   , 'G2L2-2A7':'Lights'    , 'G2L2-2A8':'GenRec'    ,
                        'G2L3-3A1':'Laundry' , 'G2L3-3A2':'HVAC'   , 'G2L3-3A3':'Laundry' , 'G2L3-3A4':'HVAC'   , 'G2L3-3A5':'Laundry'   , 'G2L3-3A6':'HVAC'      , 'G2L3-3A7':'Laundry'   , 'G2L3-3A8':'HVAC'      ,
                        'G2L3-3B1':'Laundry' , 'G2L3-3B2':'HVAC'   , 'G2L3-3B3':'Laundry' , 'G2L3-3B4':'HVAC'   , 'G2L3-3B5':'Microwave' , 'G2L3-3B6':'MakeupAir' , 'G2L3-3B7':'Microwave' , 'G2L3-3B8':'MakeupAir' ,
                    }

with open(filename, 'rU') as f:
    reader = csv.reader(f)
    #reader = csv.reader(codecs.open('file.csv', 'rU', 'utf-16'))
    reachdata = False
    meter_code_list = []
    full_list = []
    for row in reader:
    	if not reachdata:
            if not ''.join(row).strip():
                print "empty"
            else:
                if row[0]=="Time":
        			meter_code_list = row
        			reachdata = True
    	else:
    		for index, value in enumerate(row):
    		  if index is not 0:
                    meter_code = meter_code_list[index]
                    unit = MeterID_to_Unit_749[meter_code]
                    subsystem = MeterID_to_Subsys_749[meter_code]
                    full_list.append(DataPoint(row[0], unit, value, subsystem))

    #for datapt in full_list:
    #	print (datapt)

    # push into csv
    # from http://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
with open(filename[:-4] + '_output.csv', 'wb') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for datapt in full_list:
	    wr.writerow([datapt.date_time, datapt.unit, datapt.energy_use, datapt.monitor_type,])

print "DONE"
    # use sqlalchemy


#updated for use with the raw csv files received from Matt Stuart at Quadrangle Housing
import sys, re, csv, codecs, os
from os import listdir
from os.path import isfile, join

class DataPoint:
        def __init__(self, date_time, building, unit, energy_use, monitor_type):
            self.date_time = date_time
            self.building = building
            self.unit = unit
            self.energy_use = energy_use
            self.monitor_type = monitor_type
        def __str__(self):
            return (self.date_time + " " +  self.unit + " " + self.energy_use + " " + self.monitor_type)

#check for correct num args
if len(sys.argv)<2:
	sys.exit ("Usage: python sql_csv_parse_3.py [output_file_name]")

#create array of datapoints
full_list = []

for file in listdir("."):
    print(file)
    if file.endswith(".csv"):
        print("valid")
        #For 749
        #TODO: redo for both buildings
        #create dictionary between meter code and unit number for 749                                                                                                                                                                                                                        # begin 1B                  
        MeterID_to_Unit = {    #749
                               'G2L1-1A1':'1S' , 'G2L1-1A2':'1S' , 'G2L1-1A3':'1N' , 'G2L1-1A4':'1N' , 'G2L1-1A5':'1N' , 'G2L1-1A6':'2N' , 'G2L1-1A7':'2N' , 'G2L1-1A8':'2N' , 
                               'G2L1-1B1':'1S' , 'G2L1-1B2':'1S' , 'G2L1-1B3':'2S' , 'G2L1-1B4':'2S' , 'G2L1-1B5':'2S' , 'G2L1-1B6':'2S' , 'G2L1-1B7':'2N' , 'G2L1-1B8':'2N' ,
                               'G2L2-2A1':'3N' , 'G2L2-2A2':'3N' , 'G2L2-2A3':'3N' , 'G2L2-2A4':'2S' , 'G2L2-2A5':'3S' , 'G2L2-2A6':'3S' , 'G2L2-2A7':'3S' , 'G2L2-2A8':'3S' ,
                               'G2L3-3A1':'1S' , 'G2L3-3A2':'1S' , 'G2L3-3A3':'1N' , 'G2L3-3A4':'1N' , 'G2L3-3A5':'2S' , 'G2L3-3A6':'2S' , 'G2L3-3A7':'2N' , 'G2L3-3A8':'2N' ,
                               'G2L3-3B1':'3S' , 'G2L3-3B2':'3S' , 'G2L3-3B3':'3N' , 'G2L3-3B4':'3N' , 'G2L3-3B5':'N'  , 'G2L3-3B6':'N'  , 'G2L3-3B7':'S'  , 'G2L3-3B8':'S'  ,
                                #745
                               'G3L1-1A1':'1S' , 'G3L1-1A2':'1S' , 'G3L1-1A3':'1S' , 'G3L1-1A4':'1S' , 'G3L1-1A5':'1N' , 'G3L1-1A6':'1N' , 'G3L1-1A7':'1N' , 'G3L1-1A8':'1N' ,
                               'G3L1-1B1':'2S' , 'G3L1-1B2':'2S' , 'G3L1-1B3':'2S' , 'G3L1-1B4':'2S' , 'G3L1-1B5':'2N' , 'G3L1-1B6':'2N' , 'G3L1-1B7':'2N' , 'G3L1-1B8':'2N' ,
                               'G3L2-2A1':'2S' , 'G3L2-2A2':'3S' , 'G3L2-2A3':'3S' , 'G3L2-2A4':'3S' , 'G3L2-2A5':'3N' , 'G3L2-2A6':'3N' , 'G3L2-2A7':'3N' , 'G3L2-2A8':'3N' ,
                               'G3L3-3A1':'1S' , 'G3L3-3A2':'1S' , 'G3L3-3A3':'1N' , 'G3L3-3A4':'1N' , 'G3L3-3A5':'2S' , 'G3L3-3A6':'2S' , 'G3L3-3A7':'2N' , 'G3L3-3A8':'2N' ,
                               'G3L3-3B1':'3S' , 'G3L3-3B2':'3S' , 'G3L3-3B3':'3N' , 'G3L3-3B4':'3N' , 'G3L3-3B5':'Water_Heater_N' , 'G3L3-3B6':'Microwave_N' , 'G3L3-3B7':'Water_Heater_S' , 'G3L3-3B8':'Microwave_S'
                            }
        #create second dictionary between meter code and subsystem for 749
        MeterID_to_Subsys ={    #749
                                'G2L1-1A1':'GenRec'  , 'G2L1-1A2':'Spare'  , 'G2L1-1A3':'Kitchen' , 'G2L1-1A4':'Lights' , 'G2L1-1A5':'GenRec'    , 'G2L1-1A6':'Lights'    , 'G2L1-1A7':'GenRec'    , 'G2L1-1A8':'Spare1'    , 
                                'G2L1-1B1':'Kitchen' , 'G2L1-1B2':'Lights' , 'G2L1-1B3':'Kitchen' , 'G2L1-1B4':'Lights' , 'G2L1-1B5':'GenRec'    , 'G2L1-1B6':'Spare1'    , 'G2L1-1B7':'Kitchen'   , 'G2L1-1B8':'Spare2'    ,
                                'G2L2-2A1':'Kitchen' , 'G2L2-2A2':'Lights' , 'G2L2-2A3':'GenRec'  , 'G2L2-2A4':'Spare2' , 'G2L2-2A5':'Spare'     , 'G2L2-2A6':'Kitchen'   , 'G2L2-2A7':'Lights'    , 'G2L2-2A8':'GenRec'    ,
                                'G2L3-3A1':'Laundry' , 'G2L3-3A2':'HVAC'   , 'G2L3-3A3':'Laundry' , 'G2L3-3A4':'HVAC'   , 'G2L3-3A5':'Laundry'   , 'G2L3-3A6':'HVAC'      , 'G2L3-3A7':'Laundry'   , 'G2L3-3A8':'HVAC'      ,
                                'G2L3-3B1':'Laundry' , 'G2L3-3B2':'HVAC'   , 'G2L3-3B3':'Laundry' , 'G2L3-3B4':'HVAC'   , 'G2L3-3B5':'Microwave' , 'G2L3-3B6':'MakeupAir' , 'G2L3-3B7':'Microwave' , 'G2L3-3B8':'MakeupAir' ,
                                #745
                                'G3L1-1A1':'GenRec'  , 'G3L1-1A2':'Lights' , 'G3L1-1A3':'Kitchen' , 'G3L1-1A4':'Laundry' , 'G3L1-1A5':'GenRec' , 'G3L1-1A6':'Lights' , 'G3L1-1A7':'Kitchen' , 'G3L1-1A8':'Laundry' ,
                                'G3L1-1B1':'GenRec'  , 'G3L1-1B2':'Lights' , 'G3L1-1B3':'Kitchen' , 'G3L1-1B4':'Laundry' , 'G3L1-1B5':'GenRec' , 'G3L1-1B6':'Lights' , 'G3L1-1B7':'Kitchen' , 'G3L1-1B8':'Laundry' ,
                                'G3L2-2A1':'GenRec'  , 'G3L2-2A2':'Lights' , 'G3L2-2A3':'Kitchen' , 'G3L2-2A4':'Laundry' , 'G3L2-2A5':'GenRec' , 'G3L2-2A6':'Lights' , 'G3L2-2A7':'Kitchen' , 'G3L2-2A8':'Laundry' ,
                                'G3L3-3A1':'HVAC'    , 'G3L3-3A2':'Dryer'  , 'G3L3-3A3':'HVAC'    , 'G3L3-3A4':'Dryer'   , 'G3L3-3A5':'HVAC'   , 'G3L3-3A6':'Dryer'  , 'G3L3-3A7':'HVAC'    , 'G3L3-3A8':'Dryer'   ,
                                'G3L3-3B1':'HVAC'    , 'G3L3-3B2':'Dryer'  , 'G3L3-3B3':'HVAC'    , 'G3L3-3B4':'Dryer'   , 'G3L3-3B5':'Water_Heater_N' , 'G3L3-3B6':'Microwave_N' , 'G3L3-3B7':'Water_Heater_S' , 'G3L3-3B8':'Microwave_S'
                            }

        with open(file, 'rU') as f:
            reader = csv.reader(f)
            reachdata = False
            meter_code_list = []
            for row in reader:
                if not reachdata:
                    if not ''.join(row).strip():
                        print "empty row"
                    else:
                        if row[0]=="Time":
                            initial_meter_code_list = row
                            print(initial_meter_code_list)
                            for index, value in enumerate(initial_meter_code_list):
                                if len(value)==0:
                                    print "invalid meter code"
                                else:
                                    meter_code_list.append(value)
                            reachdata = True
                else:
                    for index, value in enumerate(row):
                        if index is not 0:
                            if index < len(meter_code_list):
                                meter_code = meter_code_list[index]
                                building=""
                                if "G3" in meter_code:
                                    building="749"
                                else:
                                    building="745"
                                unit = MeterID_to_Unit[meter_code]
                                subsystem = MeterID_to_Subsys[meter_code]
                                full_list.append(DataPoint(row[0], building, unit, value, subsystem))


#push into csv
#from http://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
#get output file name
output_name = sys.argv[1]
with open(output_name + '.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for datapt in full_list:
        wr.writerow([datapt.date_time, datapt.building, datapt.unit, datapt.energy_use, datapt.monitor_type])

print "DONE"
# use sqlalchemy


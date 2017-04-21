from glob import glob as g
import re
import csv

# Identify all the APM logs in the directory
files = g("*.log")

# Create empty lists
GPS = []
CAM = []

# loop through each file, split by lines
for file in files:
    handle = open(file, 'r')
    text = handle.read()
    lines = text.rstrip().split('\n')

    # Extract the data for GPS and CAM logs
    for line in lines:
        if line[0:3] == "GPS":
            line = re.sub(',','', line)
            data_list = line.split()
            data_list.insert(0,file)
            GPS.append(data_list)

        elif line[0:3] == "CAM":
            line = re.sub(',','', line)
            data_list = line.split()
            data_list.insert(0,file)
            CAM.append(data_list)

# Export flight log data from the GPS  
GPS_resultFile = open("GPS.csv",'w', newline='')
GPS_wr = csv.writer(GPS_resultFile, delimiter=',')
GPS_wr.writerows(GPS)

# Export camera logs
CAM_resultFile = open("CAM.csv",'w', newline='')
CAM_wr = csv.writer(CAM_resultFile, delimiter=',')
CAM_wr.writerows(CAM)

# Close files
GPS_resultFile.close()
CAM_resultFile.close()

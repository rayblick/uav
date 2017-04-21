# compile-flightlogs
This script extracts the data recorded on an APM ardupilot flight control board from the **GPS** and the **CAM** function. The data are compiled as a csv file named GPS.csv and CAM.csv. No headings are given. This is because I am appending the data to a MS access database. 

This code was written in Python 3.4. Note that the csv.writer method that I used to export the results to excel wont work with earlier versions of Python.

**GPS.csv contains:** 
1. file name, 
2. 'GPS', 
3. BIBcLLeeEe, 
4. Status,
5. Time,
6. NSats,
7. HDop,
8. Lat,
9. Lng,
10. RelAlt,
11. Alt,
12. Spd,
13. GCrs (compass direction)

**CAM.csv contains:**
1. file name,
2. CAM, 
3. ILLeccC, 
4. GPSTime,
5. Lat,
6. Lng,
7. Alt,
8. Roll,
9. Pitch,
10. Yaw

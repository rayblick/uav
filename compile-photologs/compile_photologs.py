import PIL.ExifTags
from PIL import Image
from glob import glob as g
import datetime as dt
import re
import csv

# find all images
images = g('*jpg')
files = g("*.log")

# create empty datastructures
photo_log = {}
first_photo = []
photo_times = []
CAM = []
first_camlog = []

# loop through each file, split by lines
for file in files:
    handle = open(file, 'r')
    text = handle.read()
    lines = text.rstrip().split('\n')

    # Extract the data for CAM log
    for line in lines:
        if line[0:3] == "CAM":
            line = re.sub(',','', line)
            data_list = line.split()
            data_list.insert(0,file)

            # Add the first GPS time to empty list [t0]
            if first_camlog == []:
                first_camlog.append(int(data_list[2]))

            time_difference = (int(data_list[2]) - first_camlog[0])/1000
            data_list.insert(1,time_difference)
            CAM.append(data_list)

# loop through all images
for i in images:
    im = Image.open(i)

    # create a dictionary containing exif data [FROM...]
    # http://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in PIL.ExifTags.TAGS
    }

    # Add datetime to empty dictionary
    photo_log[i] = exif['DateTime']
    #print(photo_log[i])
          
    # Add the first datetime to empty list [t0]
    if first_photo == []:
        first_photo.append(exif['DateTime'])

    # for every image match time stamp with first_photo [INFO FROM...]
    #http://stackoverflow.com/questions/4362491/how-do-i-check-the-difference-in-seconds-between-two-dates
    #http://stackoverflow.com/questions/1059559/python-split-strings-with-multiple-delimiters
    #https://docs.python.org/2/library/datetime.html
    #http://stackoverflow.com/questions/2711579/concatenate-strings-in-python-2-4
    #http://stackoverflow.com/questions/9504356/convert-string-into-date-type-on-python
    #Get time stamp for time zero (first photo)
    timesplit = re.findall(r"[\w']+", first_photo[0])
    timeformat = "%s/%s/%s %s:%s:%s" % (timesplit[0],timesplit[1],timesplit[2],timesplit[3],timesplit[4],timesplit[5])
    #convert to timestamp
    timestamp_t0 = dt.datetime.strptime(timeformat,"%Y/%m/%d %H:%M:%S")
    
    # get the time stamp of current image (i)
    timesplit_current_image = re.findall(r"[\w']+", photo_log[i])
    timeformat_current_image = "%s/%s/%s %s:%s:%s" % (timesplit_current_image[0],timesplit_current_image[1],timesplit_current_image[2],timesplit_current_image[3],timesplit_current_image[4],timesplit_current_image[5])
    #convert to timestamp    
    timestamp_ti = dt.datetime.strptime(timeformat_current_image,"%Y/%m/%d %H:%M:%S")

    # calculate the time difference between images
    time_diff = (timestamp_ti-timestamp_t0).total_seconds()
    photos = [i,time_diff]
    photo_times.append(photos)

# The following code came from here...[INFO FROM...]
# http://stackoverflow.com/questions/2407398/python-merge-items-of-two-lists-into-a-list-of-tuples
logs = []
place_holders = ['Null','Null']

for i in range(max((len(photo_times),len(CAM)))):
    while True:
        try:
            lg = [photo_times[i],CAM[i]]
        except IndexError:
            if len(photo_times)>len(CAM):
                CAM.append(place_holders)
                lg = [photo_times[i],CAM[i]]
            elif len(photo_times)<len(CAM):
                photo_times.append(place_holders)
                lg = [photo_times[i], CAM[i]]
            continue
        logs.append(lg)
        break

# flatten out the list of lists created above
# The list comprehension comes from here...
# http://stackoverflow.com/questions/11264684/flatten-list-of-lists
#flattened = [val for sublist in logs for val in sublist]
new_log=[]
for i in logs:
    flatten = [val for sublist in i for val in sublist]
    new_log.append(flatten)

# Export flight log data from the GPS  
logs_resultFile = open("logs.csv",'w', newline='')
logs_wr = csv.writer(logs_resultFile, delimiter=',')
logs_wr.writerows(new_log)

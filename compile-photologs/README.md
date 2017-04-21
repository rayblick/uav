# compile-photologs
Compile photo timepoints, according to image exif data, and merge the records with the camera log pulled from an APM autopilot txt file. 

This code was written to determine if there are any logs in APM data that dont have a corresponding photo. This may happen if the camera malfunctions, or the refresh rate on the camera is slower than the time between trigger events from the flight controller. The raw flight log contains lat, long, altitude, roll, pitch and yaw, which can be used in photogrammetry software for stitching photos together. Having a misisng photo in the mix can take a long time to find.

**Usage**
To use this code, copy the script to the working location containing the jpg images for one flight. Also, add to this directory the raw APM flight data as a txt file. Ensure Python 3.4 is installed on your computer. Double click the script to run. The output is a csv file containing CAM logs and image numbers merged in sequential order. 

The important details that will help determine correspondence between the flight log and photos are in the first four columns. These include the **Image Number**, **Time** since the first photo (seconds), the **Flight Log Name**, and the time since the first **GPS time** was recorded (seconds). Image times are calculated from the exif data of each photo and follows the assumption that you tested the camera before flying, which provides a known flight log and photo combination (time zero). Both time signatures are measured in seconds from time zero. 

**NOTE** It is likely that the times wont line up exactly, it is possible that there is a delay with the camera writing to exif files (this is wild speculation at this stage). However, if your camera has a refresh rate of around 2 seconds per photo then it should be reasonably easy to spot in the output.


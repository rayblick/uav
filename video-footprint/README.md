# video-footprint

Calculate video footprint from UAV positional data and gimbal angle.The total area included in the video footprint is determined by the number of data points (rows) in the input shapefile. More rows will require higher datalogging rates which will chew batteries faster on the UAV and increase processing time using this function.

Both the gimbal angle and altitude effect the total footprint size, and flight speed will ultimately determine the overlap between points. For example, the unofficial standard vehicle speed for spotlighting (from a truck) is 15 km/hr, or approximately 4 m/s. A multirotor flying at 30m altitude, carrying a gopro hero3 white camera (FOV wide = 94.4, FOV tall = 55) with a gimbal angle set at 20 degrees will provide a footprint of 65m x 37m. A multirotor flying at 4 m/s flying in a straight direction would log almost 10 datapoints at 1 second intervals until the area is traversed.

The 3dr robotics APM 2.6 can record at a rate of 0.2 seconds. As the space is limited on these boards to approximately four 12 min flights at this rate, it is recommended that the refresh rate is reduced for the purposes of this function.

Usage
1.  Import CSV file to ArcGIS with columns containing Latitude, Longitude, Altitude, Yaw, Gimbal, FOV wide, FOV tall. Columns must be in this order.
2.  Export the data as a shapefile. Import to current MXD (not required)
3.  Project the dataset to your local projection system (For NSW use GDA94 MGA zone 56)
4.  Run Video Swath tool [Requires Input and Output fields] -> must import as a script or add the UAV toolbox (to be added later)
5.  Run Dissolve function on the resultant feature class


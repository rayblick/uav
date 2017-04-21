# Generate UAVairspace
Generate a raster layer that classifies the surrounding terrain (600m r) up to 400 feet above takeoff altitude. I point out however, that this may be a redundant task once you are actually at the launch site, given that a UAV operator needs to maintain line of sight with the aircraft and you will most likely see an impending collision with high terrain. Perhaps the greatest use of this tool is in the planning stage, finding an appropriate launch site etc.

Instructions are provided in HTML within the toolbox. Download the toolbox and add it to your library. UAVairspace should appear in ArcGIS catalogue.

Briefly, the output contains a 400ft ceiling (above ground level; AGL) and a colour coded map that corresponds with the take off altitude + 400 ft above the takeoff reference point in the surrounding area (colours map blue = 3, yellow = 2, to red = 1). If you see red then you will need to account for a change in terrain otherwise you will most likely crash. 

This tool was built to identify hazardous terrain in your immediate UAV airspace. Note, in Australia, a UAV may be operated up to 600m away from the launch site with reference to 400ft (ATO) even if terrain decreases substantially. While a decrease in terrain poses its own risks, such as intercepting other aircraft, it is not considered here. 

Ideally, the output could be embedded in the ground station software.  

### Example output

![alt tag](https://cloud.githubusercontent.com/assets/9799694/6165269/51527394-b2f2-11e4-8067-7c3e65a10b7a.png)

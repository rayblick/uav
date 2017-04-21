# Construct photo footprint
Generate polygons that represent a photo footprint from xyz coordinates and a compass bearing 

Warning this code assumes that roll and pitch didn't happen. I am working on adding these parameters to the code, or though a gimbal mount would largely solve this problem for quads, and perhaps less important for the planes. Future updates will tackle oblique projection.

The code was developed with the GoPro Hero3 Black in mind. If you want to use a different sensor then you will need to manually adjust 'h' and 'w' in the code. Currently, the following specifications are hard wired into the code... 

12mp camera /standard lens, sensor 1/2.3 width 4000 x high 3000.The footprint size was first calculated in MissionPlanner software. Go pro3 footprints (@30m= 68.6 * 50.6; @50m= 114.3 * 84.3; @100m= 228.5 * 168.5; @150m= 342.8 * 252.8). I used a linear equation (with 0 intercept) to include the different altitudes of each shot during a single flight.		

### Future developments
Write a script that can be added to Arc Toolbox.

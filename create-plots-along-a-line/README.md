# create-plots-along-a-line

Construct multiple polygons representing plots from field surveys at a distance along a transect line.

This code requires some hand-processing to prepare the input data. 

Create a new geodatabase (transects.mdb) and import the shapefile from the following steps:
1) Import start and end points into ArcGIS. Make sure there is a column for joining features (e.g. TRAN1_S and TRAN1_E is given 1 and 1, TRAN2_S and TRAN2_E is given 2 and 2).
2) Use 'points to line' to create a new feature linking start and end points (include sort function by start_end position -> categorical start=0, end=1)
3) Use 'add geometry attributes (Data Management)' to add Geodesic length and bearing to the line 
4) Join tables so that transect ID and coordinates of the start position are in the line feature dataset
5) Import new dataframe, convert to shapefile and shift to geodatabase directory

### Future development
Make the script uploadable to ArcTool box.
Add transect labels and plot numbers to each polygon (e.g. S1_t1_1 - site 1, transect 1, plot 1). Currently, this info is produced but manually exported and included in the shapefile later on. 

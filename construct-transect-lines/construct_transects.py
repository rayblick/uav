# Make transect lines cross swamps

# Import system modules
import arcpy
import cmath
import math
import random
import numpy


# set up the workspace

# INPUT 1: The file path to the polygons that require scale dependent sampling  
inFeatures = arcpy.GetParameterAsText(0)

# INPUT 2: Add file path to modified polygons
modFeatures = arcpy.GetParameterAsText(1)

# OUTPUT 1: A set of transects across the modified polygons
outFeatures = arcpy.GetParameterAsText(2)

# FINAL OUTPUT: This is the OUTPUT file path for the final product including transect lines: 
outFeaturesClipped = arcpy.GetParameterAsText(3) 

# define variables
# These need to be selectable
plot_size=1	            # EDIT (meters)
plot_spacing=4		# EDIT (meters)
plot_coverage=0.006	# EDIT (percentage: here 0.6% coverage)
min_trans_dist = 50	# EDIT (meters)



features_perp=[]
fields = ("SHAPE@XY","AREA_GEO","PERIM_GEO","MBG_Width","MBG_Length","MBG_Orient","name")  

with arcpy.da.SearchCursor(modFeatures, fields) as cursor:    
    for row in cursor:	  

	# assign variable names to the imported data (call objects in fields from modFeatures)
          point_X = row[0][0]   					
          point_Y = row[0][1]   					
          swamp_area = row[1]	
          swamp_per = row[2]
          wid = row[3]
          leng = row[4]
          ori = 90-row[5]
		
	    # formula for plot spacing and replication
          # set minimum of 3 transects
          # set maximum of 8 transects
          plot_freq = swamp_area * plot_coverage
          trans_freq = (plot_freq * plot_spacing) /wid # account for the distance between plots
          if trans_freq <3:             # ensure there is a minimum number of transects per swamp
              trans_freq = 3
              min_trans_dist=20         # reduce the distance between transects so they would all fit in the swamp
          
          if trans_freq > 8:
              trans_freq = 8
              min_trans_dist=75 
                  
     
          # define stratification that retains minimum distance between transects 
          # And ensure that the number of transects doesnt overshoot the length of the swamp (or in this case the MBG units defined above) 
          max_length = leng - (trans_freq * min_trans_dist)
          rand_array = sorted(random.sample(range(0, int(max_length)), int(trans_freq)))
          dividers = (numpy.arange(int(trans_freq)) + 1) * int(min_trans_dist) 
          random_numbers = rand_array + dividers


          for i in range(0,int(trans_freq)):
              tranID = '%s_%s' %(row[6], i+1)
              print(tranID)
                          
              # find start of mid line 
              start = complex(point_X,point_Y)
              angle = ori + 180
              angle = math.radians(angle)
              movement = cmath.rect(leng/2, angle)
              end = start+movement
              endx=end.real
              endy=end.imag
              
              # Find random point
              new_start = complex(endx, endy)
              angle = ori + 0 	
              angle = math.radians(ori)	

              ran = random_numbers[i] 	# I NEED TO STRESS TEST THIS: IT MIGHT FALL ON ITS FACE

              movement = cmath.rect(ran, angle)
              new = new_start+movement
              newx=new.real
              newy=new.imag
              
              # set up an array 
              array = arcpy.Array()
             
              # corner 1 UQFM_transects_PlotNames
              pos = complex(newx,newy)
              cnr = ori + 90	 
              cnr = math.radians(cnr)	
              movement = cmath.rect(wid/2, cnr)
              end = pos+movement
              endx=end.real
              endy=end.imag
              pnt = arcpy.Point(endx,endy)        
              array.add(pnt)          
              
              # corner 2 
              pos = complex(newx,newy)
              cnr = ori + 270
              cnr = math.radians(cnr)
              movement = cmath.rect(wid/2, cnr)
              end = pos+movement
              endx=end.real
              endy=end.imag
              pnt = arcpy.Point(endx,endy)        
              array.add(pnt)     
						
              perp_line = arcpy.Polyline(array) 
              
              #print perp_line
              features_perp.append(perp_line)

		
# write to output
arcpy.CopyFeatures_management(features_perp, outFeatures)	
arcpy.Clip_analysis(outFeatures, inFeatures, outFeaturesClipped)

#===========================================================

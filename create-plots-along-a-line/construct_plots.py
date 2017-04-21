# import modules
import arcpy	  
import cmath
import math
import string

# assign fields 
inFeatures = arcpy.GetParameterAsText(0) 

# output feature class
outFeatures = arcpy.GetParameterAsText(1)

fields = ("SHAPE@XY","Bearing","Length_Geo","N","E","comment")  
# SHAPE@XY refers to coordinates for the midpoint along the line. 
# I have included the start positions and N and E to the table to account for this.

features = []

with arcpy.da.SearchCursor(inFeatures, fields) as cursor:    
	for row in cursor:	  
		#arrPnts = arcpy.Array()
		X = row[4]   					# X coordinate which matches "E"  in fields     
		Y = row[3]   					# Y coordinate which matches "N"  in fields
		A = 90-row[1]						# A stands for angle or bearing of the transect (Im not sure why these need to be adjusted by 90 degrees??)
		N = int(math.floor(row[2]/4)) 	# N is the number of plots derived from line length 
						
		for i in range(0,N+1): 		# the range defines the number of points per row
			d = i * 4				# Multiply by 4 which is the space between points
			start = complex(X,Y) 	# converts x and y coordinates to a complex number
			yaw = A	 				# The term 'yaw' is a hangover from a previous code; it refers to the direction of each point from the start position	
			yaw = math.radians(yaw)	
			movement = cmath.rect(d, yaw)
			new = start+movement
			newx=new.real
			newy=new.imag
			pnt = arcpy.Point(newx,newy)
			tranID = row[5]  # ADDED - NEED TO ATTACH TO FEATURES*****************
			print '%s_%s' %(tranID,i+1) # THIS IS A HORRIBLE DIRTY FIX - COPY to new Attribute field in the shapefile called 'new_points'*******************
			
			angle=90-row[1] 			# Setup for polygon -> This is for defining the position of points for the quadrats
			distance1 = 1 				# Setup for polygon -> points 1 and 3 from start
			distance2 = math.sqrt(distance1**2 + distance1**2)		# Setup for polygon -> calculate hypotenuse for the point that is diagonal to the start position 
			arrPnts = arcpy.Array()     # Setup for polygon -> this is where each of the points will get saved, before becoming a feature
			
			
			# corner 1 
			pos = complex(newx,newy) # converts x and y coordinates to a complex number
			cnr = angle + 0		 # cnr refers to the direction of each point from the start position	
			cnr = math.radians(cnr)	
			movement = cmath.rect(distance1, cnr)
			end = pos+movement
			endx=end.real
			endy=end.imag
			pnt = arcpy.Point(endx,endy)        
			arrPnts.add(pnt)          

			# corner 2 
			pos = complex(newx,newy)
			cnr = angle + 45
			cnr = math.radians(cnr)
			movement = cmath.rect(distance2, cnr)
			end = pos+movement
			endx=end.real
			endy=end.imag
			pnt = arcpy.Point(endx,endy)        
			arrPnts.add(pnt)        

			# corner 3  
			pos = complex(newx,newy)
			cnr = angle + 90 
			cnr=math.radians(cnr)
			movement = cmath.rect(distance1, cnr)
			end = pos+movement
			endx=end.real
			endy=end.imag
			pnt = arcpy.Point(endx,endy)        
			arrPnts.add(pnt)         

			# corner 4 
			pos = complex(newx,newy)
			cnr = angle 
			cnr = math.radians(cnr)	
			movement = cmath.rect(0, cnr)
			end = pos+movement
			endx=end.real
			endy=end.imag
			pnt = arcpy.Point(endx,endy)        
			arrPnts.add(pnt)         
			
			pol = arcpy.Polygon(arrPnts) 
			features.append(pol)

# write to output
arcpy.CopyFeatures_management(features, outFeatures)



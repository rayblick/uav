# Import system modules
import arcpy
import cmath
import math

# For ArcTool construction comment out the above line and use the following line.
flightlog = arcpy.GetParameterAsText(0)

# assign each field that will be used for calculation.
fields = ("SHAPE@XY","lat","long","alt","yaw","gimbal","fov_wide","fov_tall")  		

# OR select output destination
fcout = arcpy.GetParameterAsText(1)

# create an empty list
features = []

# search row by row in the dataset and generate video swath
with arcpy.da.SearchCursor(flightlog, fields) as cursor:    
	for row in cursor:
		# assign lat and long coordinates to X and Y
		X = row[0][0]        
		Y = row[0][1]
		
		# assign columns to position of aircraft
		alt=row[3]
		angle=row[4]

		# assign columns to camera parameters
		gimbalx=0
		gimbaly=row[5]
		fov_width=row[6]
		fov_height=row[7]

		# Calculate the distance of each edge of footprint rectangle 
		top = alt * math.tan(math.radians(gimbaly + 0.5 * fov_height))
		bottom = alt * math.tan(math.radians(gimbaly - 0.5 * fov_height))
		right = alt * math.tan(math.radians(gimbalx + 0.5 * fov_width))
		left = alt * math.tan(math.radians(gimbalx - 0.5 * fov_width))

		# Find the distance to each corner
		topL_distance=(math.sqrt(left**2+top**2))
		topR_distance=(math.sqrt(right**2+top**2))
		bottomL_distance=(math.sqrt(left**2+bottom**2)) 
		bottomR_distance=(math.sqrt(right**2+bottom**2)) 

		# calculate angles to corners
		p1 = 180 * math.atan(right/top) / math.pi # right/top
		p2 = 180 * math.atan(bottom/right) / math.pi #bottom/right
		p3 = 180 * math.atan(left/bottom)/ math.pi #bottom/left
		p4 = 180 * math.atan(top/left)/ math.pi #left/top
		print(p1,p2,p3,p4)
		
		# Create empty array called arrPnts
		arrPnts = arcpy.Array()        

		# point 1 [top right]
		start = complex(X,Y)
		# Top right angle = inverse tangent of width (opposite) / height (adjacent)
		# convert to degrees to add to the existing yaw angle
		yaw = angle + 0 + p1
		yaw = 90 - yaw
		if yaw < -180: 
			yaw = 360 + yaw
		
		yaw=math.radians(yaw)	
		# convert polar coordinates to rectangular coordinates using cmath.rect
		movement = cmath.rect(topR_distance, yaw)
		end = start+movement
		endx=end.real
		endy=end.imag
		pnt = arcpy.Point(endx,endy)        
		arrPnts.add(pnt)        

		# point 2 [bottom right]
		start = complex(X,Y)
		# bottom right angle = inverse tangent of height (opposite) / width (adjacent)
		# convert to degrees to add to the existing yaw angle
		yaw = angle + 90 - p2
		yaw = 90 - yaw
		if yaw < -180: 
			yaw = 360 + yaw

		yaw=math.radians(yaw)
		movement = cmath.rect(bottomR_distance, yaw)
		end = start+movement
		endx=end.real
		endy=end.imag
		pnt = arcpy.Point(endx,endy)        
		arrPnts.add(pnt)        

		# point 3 [bottom left]
		start = complex(X,Y)
		# bottom left angle = inverse tangent of height (opposite) / width (adjacent)
		# convert to degrees to add to the existing yaw angle
		
		# **NOTE**
		# This corner required additional computation. Due to the fact that I have located each
		# corner by segmenting the polygon into four quadrats, this point can move in front of
		# the UABV position. This means that a positive value can become negative and the 
		# computation breaks. I have modified the start position (angle + 180 + p3) if the 
		# angle becomes negative. I found this problem when I set the gimbal angle to anything
		# above ~27 degrees.
		if p3 < 0: 
			yaw = angle + 0 + p3
			yaw = 90 - yaw
		else:
			yaw = angle + 180 + p3	
			yaw = 90 - yaw
		
		if yaw < -180: 
			yaw = 360 + yaw
		
		yaw=math.radians(yaw)
		movement = cmath.rect(bottomL_distance, yaw)
		end = start+movement
		endx=end.real
		endy=end.imag
		pnt = arcpy.Point(endx,endy)        
		arrPnts.add(pnt)         

		# point 4 [top left]
		start = complex(X,Y)
		# Top right angle = inverse tangent of width (opposite) / height (adjacent)
		# convert to degrees to add to the existing yaw angle
		yaw = angle + 270 - p4
		yaw = 90 - yaw
		if yaw < -180: 
			yaw = 360 + yaw
			
		yaw=math.radians(yaw)	
		movement = cmath.rect(topL_distance, yaw)
		end = start+movement
		endx=end.real
		endy=end.imag
		pnt = arcpy.Point(endx,endy)        
		arrPnts.add(pnt)         

		pol = arcpy.Polygon(arrPnts)        
		features.append(pol)

# write to output
arcpy.CopyFeatures_management(features, fcout)

# import the new layer
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
sourceLayer = arcpy.mapping.Layer(fcout)
arcpy.mapping.AddLayer(df,sourceLayer,"TOP")
arcpy.RefreshActiveView()

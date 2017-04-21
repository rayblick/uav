import arcpy	  
import cmath
import math
camlog = r'C:\Program Files (x86)\Raytest\new1.gdb\camlog' # EDIT THIS (camlog is a shapefile)
fields = ("SHAPE@XY","b","z")  		
	  
# output feature class
fcout = r'C:\Program Files (x86)\Raytest\new1.gdb\area02' # EDIT THIS (area02 is a polygon feature)
features = []
with arcpy.da.SearchCursor(camlog, fields) as cursor:    
	for row in cursor:
		angle=row[1]
		altitude=row[2]
		h=1.6853*altitude 
		w=2.285*altitude
		distance=(math.sqrt(w**2+h**2))/2 
		arrPnts = arcpy.Array()        
		X = row[0][0]        
		Y = row[0][1]
		rad2deg=180/math.pi
		
		# point 1 
		start = complex(X,Y)
		yaw = angle + 0 + (math.atan((w/2) / (h/2))*rad2deg)
		yaw = 90 - yaw
		if yaw < -180: 
			yaw = 360 + yaw
		yaw=math.radians(yaw)	
		movement = cmath.rect(distance, yaw)
		end = start+movement
		endx=end.real
		endy=end.imag
		pnt = arcpy.Point(endx,endy)        
		arrPnts.add(pnt)        

		# point 2 
		start = complex(X,Y)
		yaw = angle + 90 + (math.atan((h/2)/(w/2))*rad2deg)
		yaw = 90 - yaw
		if yaw < -180: 
			yaw = 360 + yaw
		yaw=math.radians(yaw)
		movement = cmath.rect(distance, yaw)
		end = start+movement
		endx=end.real
		endy=end.imag
		pnt = arcpy.Point(endx,endy)        
		arrPnts.add(pnt)        

		# point 3  
		start = complex(X,Y)
		yaw = angle + 180 +(math.atan((w/2)/(h/2))*rad2deg)
		yaw = 90 - yaw
		if yaw < -180: 
			yaw = 360 + yaw
		yaw=math.radians(yaw)
		movement = cmath.rect(distance, yaw)
		end = start+movement
		endx=end.real
		endy=end.imag
		pnt = arcpy.Point(endx,endy)        
		arrPnts.add(pnt)         

		# point 4 
		start = complex(X,Y)
		yaw = angle + 270 +(math.atan((h/2)/(w/2))*rad2deg)
		yaw = 90 - yaw
		if yaw < -180: 
			yaw = 360 + yaw
		yaw=math.radians(yaw)	
		movement = cmath.rect(distance, yaw)
		end = start+movement
		endx=end.real
		endy=end.imag
		pnt = arcpy.Point(endx,endy)        
		arrPnts.add(pnt)         

		pol = arcpy.Polygon(arrPnts)        
		features.append(pol)

# write to output
arcpy.CopyFeatures_management(features, fcout)

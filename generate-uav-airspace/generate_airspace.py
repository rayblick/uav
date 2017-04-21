# Import system modules
import arcpy

# INPUT 1: add takeoff point  
# point shapefile containing all takeoff points (X and Y) requiring airspace
inATO = arcpy.GetParameterAsText(0)

# INPUT 2: add the aster layer
inDEM = arcpy.GetParameterAsText(1)

# OUTPUT 1: for buffer 
outBuff = arcpy.GetParameterAsText(2)

# OUTPUT 2: select output destination
outFeatures = arcpy.GetParameterAsText(3)

# Flight rules (m)
flightArea=600
flightAlt=121.92

# get the altitude of the waypoint (MUST HAVE 'Z" from Add surface attributes)
field="Z"
values = [row[0] for row in arcpy.da.SearchCursor(inATO, (field))]
getATO= values[0]

# preliminary setup
arcpy.Buffer_analysis(inATO, outBuff, flightArea)
arcpy.Clip_management(inDEM,"#",outFeatures,outBuff,0,"ClippingGeometry")

# set local variables
fieldName1 = "ceiling"
fieldName2 = "colourCode"
fieldName3 = "ATO"

# colour codes
# if take off reference point + 375 ft (114.3) is lower than DEM Value then its RED (1)
# if take off reference point + 325 ft (99.06) is greater than DEM then its blue (3)
# otherwise if the ATO + (325 to 375 ft) is lower than DEM value then its YELLOW (2) 

#Execute add field
arcpy.AddField_management(outFeatures,fieldName1,"Double")
arcpy.AddField_management(outFeatures,fieldName2,"Double")

# add the reference point for Takeoff to each row in the raster layer
arcpy.AddField_management(outFeatures,fieldName3,"Double")


# add the cieling height
fields = ["Value","ceiling","colourCode","ATO"] 

with arcpy.da.UpdateCursor(outFeatures,fields) as cursor:
    for row in cursor:
        row[3] = getATO
        row[1] = row[0] + flightAlt
        if (row[3] + 114.3) < row[0]:
            row[2]=1
        elif (row[3] + 99.06) > row[0]:
            row[2]=3
        else:
            row[2]=2
        cursor.updateRow(row) 

# import the new raster layer
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
sourceLayer = arcpy.mapping.Layer(outFeatures)
arcpy.mapping.AddLayer(df,sourceLayer,"TOP")
arcpy.RefreshActiveView()

# update output with symbology according to elevation (red, yellow and blue)
str = outFeatures
indexForStr = str.rfind('\\')

mySymb = outFeatures[0:indexForStr] + "\\colourMap.lyr"
layerSymb=arcpy.mapping.Layer(mySymb)
updateLayer=arcpy.mapping.ListLayers(mxd,sourceLayer,df)[0]
arcpy.mapping.UpdateLayer(df,updateLayer,layerSymb,"TRUE")
arcpy.RefreshTOC()

"""
Author: Hitomi Nakamura
Date: 6/1/2020
Edit Date: 6/16/2020
Project Name: GWW Segment D1
---Note---
This script creates survey area buffer
"""
import arcpy
import os
import time

start_time = time.time()

arcpy.env.overwriteOutput = True

#database
database = arcpy.GetParameterAsText(0)#r"C:\Users\hitomi.nakamura\Documents\GWWD1_base\GWWD1_base.gdb"
arcpy.env.workspace = database
arcpy.Delete_management("memory")

# cl = arcpy.GetParameterAsText(1)#"Centerline"
accessRoads = arcpy.GetParameterAsText(1)#"Access_Roads"
disturbance = arcpy.GetParameterAsText(2)#"Disturbance_Areas"
boreholes = arcpy.GetParameterAsText(3)#"Boreholes"
substation = arcpy.GetParameterAsText(4)#"Substation_Locations"
ROW_Polygon = arcpy.GetParameterAsText(5)

'''
####--------Create ROW_Polygon---------####
#make feature layer without existing alignment
cl_sql = "Subtype <> 'Existing Alignment'"
cl_select = "cl_select"
arcpy.MakeFeatureLayer_management(cl, cl_select, cl_sql)
#dissolve cl
cl_dissolve = "memory/cl_dissolve"
arcpy.Dissolve_management(cl_select, cl_dissolve)
#create graphic buffer
cl_buffer = "memory/cl_buffer"
arcpy.GraphicBuffer_analysis(cl_dissolve, cl_buffer, "62.5 Feet", "BUTT", "MITER", 10)
#dissolve the buffer
ROW_Polygon = "utilitiesCommunicationPod/ROW_Polygon"
arcpy.Dissolve_management(cl_buffer,ROW_Polygon)
'''
####--------Create dissolved access roads---------####
#make feature without existing roads and specific OID
ar_sql = "(OBJECTID <> 27 And OBJECTID <> 28 And OBJECTID <> 29 And OBJECTID <> 30 And OBJECTID <> 31 And OBJECTID <> 32 And OBJECTID <> 36 And OBJECTID <> 37) And (Subtype = 'Improve Existing' Or Subtype = 'New Road' Or Subtype = 'Secondary' Or Subtype = 'Temporary')"
accessRoads_select = "accessRoads_select"
arcpy.MakeFeatureLayer_management(accessRoads,accessRoads_select, ar_sql)
ar_dissolve = "memory/ar_dissolve"
arcpy.Dissolve_management(accessRoads_select,ar_dissolve)

####--------Create boreholes with active but not completed status---------####
bh_sql = "Status = 'Active' And Complete = 'No'"
bh_select = "bh_select"
arcpy.MakeFeatureLayer_management(boreholes, bh_select, bh_sql)

####--------Disturbance Area with temporary work areas for 50ft buffer---------####
temp_sql = "Type <> 'Structure Work Area' And Type <> 'Regen Site'"
temp_select = "temp_select"
arcpy.MakeFeatureLayer_management(disturbance, temp_select, temp_sql)
####--------Disturbance Area with only structure work areas for 100ft buffer---------####
str_sql = "Type = 'Structure Work Area' Or Type = 'Regen Site'"
str_select = "str_select"
arcpy.MakeFeatureLayer_management(disturbance, str_select, str_sql)
####--------Union disturbance area and ROW Polygon---------####
ROW_disturbance = "memory/ROW_disturbance"
arcpy.Union_analysis([ROW_Polygon,disturbance],ROW_disturbance,"ALL")

####--------Buffer function--------####
def buffer(inList, distance, unit):
    distance_unit = "{} {}".format(distance,unit)
    outList = []
    for i in inList:
        if "memory/" in i:
            n = i[7:]
        else:
            n = i
        outName = "memory/{}{}{}buffer".format(n[:3],str(distance).replace(".",""),unit)
        if arcpy.Describe(i).shapeType == "Polygon" or arcpy.Describe(i).shapeType == "Point":
            arcpy.Buffer_analysis(i, outName, distance_unit, "FULL", None,"ALL")
        else:
            arcpy.Buffer_analysis(i,outName, distance_unit, "FULL","ROUND","ALL")
        outList.append(outName)
    return outList

####--------merge and dissolve function--------####
def merge(inList, outName):
    mergeName = "memory/merge_{}".format(outName[26:])
    arcpy.Merge_management(inList, mergeName)
    arcpy.Dissolve_management(mergeName, outName)
    return outName

def addFieldPopulate(inFeature, inPopulate):
    buffDist = "bufferDistance"
    buffDistAlias = "Buffer Distance"
    applicable = "applicableSpecies"
    applicableAlias = "Applicable Species"
    updateField = [buffDist,applicable]
    #add field name bufferDistance
    arcpy.AddField_management(inFeature, buffDist, "TEXT","","",100,buffDistAlias)
    #add field name applicableSpecies
    arcpy.AddField_management(inFeature, applicable, "TEXT","","",100, applicableAlias)
    buffPopulate = inPopulate[0]
    appliPopulate = inPopulate[1]
    arcpy.CalculateField_management(inFeature,buffDist, buffPopulate)
    arcpy.CalculateField_management(inFeature,applicable,appliPopulate)
    # #update cursor
    # with arcpy.da.UpdateCursor(inFeature, updateField) as cursor:
    #     for row in cursor:
    #         row[0] = buffPopulate
    #         row[1] = appliPopulate
    #     cursor.updateRow(row)

####--------100-m buffer for sensitive plant habitat assessments--------####
#create buffer list
bufferAll = [ROW_disturbance, ar_dissolve, bh_select]
distance100 = 100
unit_meter = "Meters"
buffer100m = buffer(bufferAll, distance100, unit_meter)
#merge list and dissolve
final100m = "utilitiesCommunicationPod/Plant_Habitat_Buffer"
merge100m = merge(buffer100m, final100m)


####--------0.25-mile buffer for Prairie Dogs--------####
distance025 = 0.25
unit_miles = "Miles"
buffer025miles = buffer(bufferAll, distance025, unit_miles)
#merge list and dissolve
final025mi = "utilitiesCommunicationPod/Prairie_Dogs_Buffer"
merge025mi = merge(buffer025miles,final025mi)

####--------0.75-mile buffer for Burrowing Owl--------####
distance075 = 0.75
buffer075miles = buffer(bufferAll, distance075, unit_miles)
#merge list and dissolve
final075mi = "utilitiesCommunicationPod/Burrowing_Owl_Buffer"
merge075mi = merge(buffer075miles,final075mi)


####--------100-ft and 50-ft buffer for noxious weeds--------####
#100ft
buffer100ftList = [substation, bh_select, str_select]
unit_ft = "Feet"
buffer100ft = buffer(buffer100ftList,distance100, unit_ft)
#50ft
buffer50ftList = [temp_select, ar_dissolve]
distance50 = 50
buffer50ft = buffer(buffer50ftList, distance50, unit_ft)

#merge 100ft list, 50ft list and ROW_Polygon
noxiousBuffer = buffer100ft + buffer50ft
noxiousBuffer.append(ROW_Polygon)

#merge list and dissolve
finalNoxious = "utilitiesCommunicationPod/Noxious_Weeds_Buffer"
mergeNoxious = merge(noxiousBuffer, finalNoxious)

#add fields and populate
buffField100 = "'{} {}'".format(str(distance100),unit_meter)
buffField025 = "'{} {}'".format(str(distance025),unit_miles)
buffField075 = "'{} {}'".format(str(distance075),unit_miles)
buffFieldNox = "'50 to 100 {}'".format(unit_ft)
populate100m = [buffField100, "'Plant Habitat'"]
populate025mi = [buffField025, "'Prairie Dogs'"]
populate075mi = [buffField075, "'Burrowing Owls'"]
populateNoxious = [buffFieldNox, "'Noxious Weeds'"]
#send to function
addFieldPopulate(final100m, populate100m)
addFieldPopulate(final025mi, populate025mi)
addFieldPopulate(final075mi, populate075mi)
addFieldPopulate(finalNoxious, populateNoxious)

#merge all buffers
finalMerge = [final075mi, final025mi, final100m, finalNoxious]
finalOutput = arcpy.GetParameterAsText(6)
arcpy.Merge_management(finalMerge,finalOutput)
arcpy.Delete_management(final075mi)
arcpy.Delete_management(final025mi)
arcpy.Delete_management(final100m)
arcpy.Delete_management(finalNoxious)


#print final message
arcpy.AddMessage("All done")
end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
arcpy.AddMessage('Completed in {} minutes.'.format(ttl_time))
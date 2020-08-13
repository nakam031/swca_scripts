"""
Author: Hitomi Nakamura
Date: 6/16/2020
Edit Date: 6/16/2020
Project Name: #####
---Note---
This script is creates ROW polygon specifically for #####
"""

import arcpy
import os
import time

start_time = time.time()

arcpy.env.overwriteOutput = True

#database
# database = arcpy.GetParameterAsText(0)#r"C:\Users\hitomi.nakamura\Documents\GWWD1_base\GWWD1_base.gdb"
# arcpy.env.workspace = database
arcpy.Delete_management("memory")

cl = arcpy.GetParameterAsText(0)#"Centerline"
outFeature = arcpy.GetParameterAsText(1)

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
# ROW_Polygon = "ROW_Polygon"
arcpy.Dissolve_management(cl_buffer,outFeature)

arcpy.AddMessage("All done")
end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
arcpy.AddMessage('Completed in {} minutes.'.format(ttl_time))

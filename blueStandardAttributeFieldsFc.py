"""
Author: Hitomi Nakamura
Date: 6/18/2020
Edit Date: 6/24/2020
Project Name: GWW Segment D1
---Note---
This script will add all the required attribute fields from SWCA standard to the feature classes.
Input can be multiple feature classes.

"""

import arcpy
import time
import pandas as pd
start_time = time.time()
#input features can be multiple
fcList = arcpy.GetParameterAsText(0)
fcList = fcList.split(";")
arcpy.env.overwriteOutput = True


polygon_df = pd.read_excel(r"N:\Projects\15000\15915_18_GatewayWestSegmentD1\assets\pythonScript\tableUsedForScript\SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='PolygonFeatureClass')
# header = list(df.columns)
polygon_df = polygon_df.fillna("")
polygon_ls = polygon_df.values.tolist()
linear_df = pd.read_excel(r"N:\Projects\15000\15915_18_GatewayWestSegmentD1\assets\pythonScript\tableUsedForScript\SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='LinearFeatureClass')
linear_df = linear_df.fillna("")
linear_ls = linear_df.values.tolist()
point_df = pd.read_excel(r"N:\Projects\15000\15915_18_GatewayWestSegmentD1\assets\pythonScript\tableUsedForScript\SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='PointFeatureClass')
point_df = point_df.fillna("")
point_ls = point_df.values.tolist()

    

for fc in fcList:
    print(fc)
    if arcpy.Describe(fc).shapeType == "Polygon":
        dc = polygon_ls
    elif arcpy.Describe(fc).shapeType == "Polyline":
        dc = linear_ls
    elif arcpy.Describe(fc).shapeType == "Point":
        dc = point_ls

    fields = [f.name for f in arcpy.ListFields(fc)]
    fields = [f.lower() for f in fields]
    arcpy.AddMessage("fields {}".format(fields))
    for d in dc:
        # print("d: {}".format(d))
        key = d[0]
        # arcpy.AddMessage("key {}".format(key.upper()))
        if key.lower() in fields:
            pass
        else:
            arcpy.AddMessage("key {}".format(key.upper()))
            fieldName = d[0]
            fieldAlias = d[1]
            fieldType = d[2]
            if d[3] != "":
                fieldLength = int(d[3])
            else:
                fieldLength = d[3]

            arcpy.AddField_management(fc,fieldName,fieldType, "", "", fieldLength, fieldAlias)



arcpy.AddMessage("All done")
end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
arcpy.AddMessage('Completed in {} minutes.'.format(ttl_time))
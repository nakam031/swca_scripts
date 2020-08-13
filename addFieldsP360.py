#########Summary of this script#########
"""
Author: Hitomi Nakamura
Date: 6/8/2020
Edit Date: 7/8/2020
Project Name: ########
---Note---
This script will add all the required attribute fields from P360 standards to the feature classes in the gdb.
This will apply to all the feature classes in the gdb. If you want to apply to individual feature class, please use "Add_Fields_P360_fc.py"

"""

import arcpy
import time
import os
start_time = time.time()
database = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True
arcpy.env.workspace = database

#required attribute table
dc = [["Unique_ID","TEXT",50,"Unique ID"],["Type","TEXT",50, "Type"],["Subtype","TEXT",50,"Subtype"],
["Created_Date","DATE",None, "Created Date"],["Created_By","TEXT",15,"Created By"],["Modified_Date","DATE",None,"Modified Date"],
["Modified_By","TEXT",15,"Modified By"],["Modified_Note","TEXT",50,"Modified Note"],["Archived_Date","DATE",None, "Archived Date"],
["Archived_By","TEXT",15,"Archived By"],["Archived_Note","TEXT",50,"Archived Note"],["Source_Date","DATE",None,"Source Date"],
["Accuracy","TEXT",15,"Accuracy"],["Internal_Use","TEXT",25,"Internal Use"],["Data_Source","TEXT",50,"Data Source"],
["Status","TEXT",10,"Status"],["Survey_Type","TEXT",50,"Survey Type"],["Notes","TEXT",250, "Notes"]]
#create a list of feature classes in dataset
def addFields(fcList):
    for fc in fcList:
        fields = [f.name for f in arcpy.ListFields(fc)]
        
        for d in dc:
            # print("d: {}".format(d))
            if d[0] in fields:
                pass
            else:
                arcpy.AddField_management(fc,field_name = d[0],field_type = d[1], field_precision = None, field_scale = None, field_length = d[2], field_alias = d[3])

dataType = arcpy.Describe(database).dataType
if dataType == "FeatureDataset":
    fcl = arcpy.ListFeatureClasses()
    if len(fcl) > 0:
        addFields(fcl)
    else:
        pass

elif dataType == "Workspace":

    fcl = arcpy.ListFeatureClasses()
    if len(fcl) > 0:
        addFields(fcl)
    else:
        pass

    datasets = arcpy.ListDatasets("*", "Feature")

    if len(datasets) > 0:
        for d in datasets:
            fcList = arcpy.ListFeatureClasses(feature_dataset = d)
            if len(fcList) > 0:
                addFields(fcList)
            else:
                arcpy.AddMessage("Dataset: {} is empty".format(d))


arcpy.AddMessage("All done")
end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
arcpy.AddMessage('Completed in {} minutes.'.format(ttl_time))

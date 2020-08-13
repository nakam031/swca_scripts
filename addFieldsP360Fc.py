#########Summary of this script#########
"""
Author: Hitomi Nakamura
Date: 6/10/2020
Edot Date: 6/10/2020
Project Name: #######
---Note---
This script will add all the required attribute fields from P360 standards to the feature class.
This will apply to the input feature class. If you want to apply to all the feature classes in the gdb, please use "Add_Fields_P360.py"

"""
import arcpy
import time

start_time = time.time()
#input is a feature class
fcs = arcpy.GetParameterAsText(0)
fcs = fcs.split(";")
arcpy.AddMessage(fcs)
arcpy.env.overwriteOutput = True

#required attribute table
dc = [["Unique_ID","TEXT",50,"Unique ID"],["Type","TEXT",50, "Type"],["Subtype","TEXT",50,"Subtype"],
["Created_Date","DATE",None, "Created Date"],["Created_By","TEXT",15,"Created By"],["Modified_Date","DATE",None,"Modified Date"],
["Modified_By","TEXT",15,"Modified By"],["Modified_Note","TEXT",50,"Modified Note"],["Archived_Date","DATE",None, "Archived Date"],
["Archived_By","TEXT",15,"Archived By"],["Archived_Note","TEXT",50,"Archived Note"],["Source_Date","DATE",None,"Source Date"],
["Accuracy","TEXT",15,"Accuracy"],["Internal_Use","TEXT",25,"Internal Use"],["Data_Source","TEXT",50,"Data Source"],
["Status","TEXT",10,"Status"],["Survey_Type","TEXT",50,"Survey Type"],["Notes","TEXT",250, "Notes"]]
#create a list of fields in feature class
for fc in fcs:
    fc = fc.replace("'","")
    fields = [f.name for f in arcpy.ListFields(fc)]
    i = 0
    arcpy.AddMessage(fc)
    for d in dc:
    # print("d: {}".format(d))
        if d[0] in fields:
            pass
        else:
            arcpy.AddField_management(fc,field_name = d[0],field_type = d[1], field_precision = None, field_scale = None, field_length = d[2], field_alias = d[3])


arcpy.AddMessage("All done")
end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
arcpy.AddMessage('Completed in {} minutes.'.format(ttl_time))

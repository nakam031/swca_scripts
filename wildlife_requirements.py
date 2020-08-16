import arcpy
import os
import pandas as pd
import time

start_time = time.time()

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r'N:\Projects\48000\48649_TransWest\Data\GIS\Outputs_Clipped.gdb'

excelPath = "N:\\Projects\\48000\\48649_TransWest\\Data\\Tables\\mapping_requirement_wildlife.xlsx"
outFeature = "N:\\Projects\\48000\\48649_TransWest\\Data\\GIS\\Outputs_Clipped.gdb\\Wildlife_Constraints_Union"

df = pd.read_excel(excelPath, sheet_name='ROD Reqmts Tabulation', usecols=['FeatureName','Dataset'])
ls = df.values.tolist()
# print(ls)

featureList = []
for l in ls:
    featurePath = "{}\\{}".format(l[1],l[0])
    if arcpy.Exists(featurePath):
        featureList.append(featurePath)
    else:
        pass

try:

    print("start_union")
    updateCol = "Legend_Name"
    arcpy.Union_analysis(featureList,outFeature,"ALL")
    legendField = arcpy.ListFields(outFeature,updateCol)
    if len(legendField) != 1:
        arcpy.AddField_management(outFeature, updateCol, "TEXT")
    else:
        pass

    delList = []
    key = "FID_"
    listFields = arcpy.ListFields(outFeature)
    for f in listFields:
        if not f.required:
            if key.upper() in f.name.upper():
                delList.append(f.name)
            else:
                pass
    
    if len(delList) > 0:
        arcpy.DeleteField_management(outFeature, delList)
    
    newList = arcpy.ListFields(outFeature)
    reqList = [req.name for req in newList if 'req_num' in req.name]
    length = len(reqList)
    updateList = reqList
    updateList.append(updateCol)
    # print(reqList)

    with arcpy.da.UpdateCursor(outFeature,updateList) as cursor:
    
        for row in cursor:
            rowList = []
            i = 0
            while i <= length:
                rowList.append(row[i])
                i += 1
            updateLegend = ', '.join(filter(None, rowList))
            # print(updateLegend)
            row[len(updateList)-1] = updateLegend
            cursor.updateRow(row)


    

except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

finally:
    print("done")
    end_time = time.time()
    ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
    print('Completed in {} minutes.'.format(ttl_time))
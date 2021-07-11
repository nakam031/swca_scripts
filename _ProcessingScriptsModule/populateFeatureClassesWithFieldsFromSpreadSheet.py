"""
Author: Hitomi Nakamura
Date: 4/2/2020

Project Name: Standard
---Note---
This script will create wetland polygon, line with domains (reads all the information from separate spreadsheet)

"""

import arcpy
import time
import pandas as pd
import sys
import os
import blueStandardAttributeFieldsFc
start_time = time.time()
#input
folder = r'N:\gisTools\Development\Python_Development_HitomiN\exampleFiles\testFolder\FC'#arcpy.GetParameterAsText(0)
fileList = ""#arcpy.GetParameterAsText(1)
appendList = []
if folder != "" or folder != []:
    for infile in os.listdir(folder):
        if infile.endswith(".xlsx"):
            outpath = os.path.join(folder,infile)
            appendList.append(outpath)
elif fileList != []:
    appendList = fileList

for spreadsheet in appendList:
    sheetLists = pd.read_excel(spreadsheet,sheet_name=None).keys()

    if "POLYGONFeatureClass" in sheetLists:
        sheetFeatureClass = "POLYGONFeatureClass"
    elif "POLYLINEFeatureClass" in sheetLists:
        sheetFeatureClass = "POLYLINEFeatureClass"
    elif "POINTFeatureClass" in sheetLists:
        sheetFeatureClass = "POINTFeatureClass"
    elif "MULTIPOINTFeatureClass" in sheetLists:
        sheetFeatureClass = "MULTIPOINTFeatureClass"
    else:
        sys.exit("There is an error in spreadsheet.")
    arcpy.env.overwriteOutput = True
    #master sheet to get fc info
    master_df = pd.read_excel(spreadsheet,sheet_name='Master')
    fc = master_df['Feature Class Location'][0]
    database = fc.split('.gdb')[0] + '.gdb'
    geometryType = master_df['Geometry Type'][0]
    blueStandardAttributeFieldsFc.blueStandardAddField(fc,database)

    #domain dictionary
    if "Domain" in sheetLists:
        domainMaster_df= pd.read_excel(spreadsheet,sheet_name='Domain')

        domainMaster_list = domainMaster_df.values.tolist()

        #create domain
        desc = arcpy.Describe(database)
        domain = desc.domains

        for domainMaster in domainMaster_list:
            domainMasterName = domainMaster[0]
            domainMasterDescription = domainMaster[1]
            domainMasterType = domainMaster[2]
            if domainMasterName not in domain:
                arcpy.CreateDomain_management(database,domainMasterName,domainMasterDescription,domainMasterType,"CODED")
                df = pd.read_excel(spreadsheet,sheet_name=domainMasterName,index_col=0)
                df_dict = df.to_dict()["DESCRIPTION"]
                for code in df_dict:
                    arcpy.AddCodedValueToDomain_management(database,domainMasterName,code,df_dict[code])


    #access to spreadsheet for fields properties
    feature_df = pd.read_excel(spreadsheet,sheet_name=sheetFeatureClass)
    # header = list(df.columns)
    feature_df = feature_df.fillna("")
    feature_ls = feature_df.values.tolist()
        
    fields = [f.name for f in arcpy.ListFields(fc)]
    fields = [f.lower() for f in fields]
    # arcpy.AddMessage("fields {}".format(fields))
    for d in feature_ls:
        # print("d: {}".format(d))
        key = d[0]
        # arcpy.AddMessage("key {}".format(key.upper()))
        if key.lower() in fields:
            pass
        else:
            # arcpy.AddMessage("key {}".format(key.upper()))
            fieldName = d[0]
            fieldAlias = d[1]
            fieldType = d[2]
            fieldDomain = d[4]
            if d[3] != "":
                fieldLength = int(d[3])
            else:
                fieldLength = d[3]

            arcpy.AddField_management(fc,fieldName,field_type=fieldType, field_length=fieldLength, field_alias=fieldAlias)
            if fieldDomain != "NONE":
                arcpy.AssignDomainToField_management(fc, fieldName,fieldDomain)

end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
arcpy.AddMessage('Completed in {} minutes.'.format(ttl_time))



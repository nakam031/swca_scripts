"""
Author: Hitomi Nakamura
Date: 6/16/2020
Edit Date: 6/17/2020
Project Name: ######
---Note---
This script will add all the domains to the gdb and apply to applicable fields in the feature classes.

"""

import arcpy
import time
import pandas as pd
start_time = time.time()
inputData = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True
arcpy.env.workspace = inputData
dataType = arcpy.Describe(inputData).dataType
if dataType == "FeatureDataset":
    database = arcpy.Describe(inputData).path
elif dataType == "Workspace":
    database = inputData


#domain dictionary
AreaUom_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='AreaUom',index_col=0)#replace with filepath
LengthUom_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='LengthUom',index_col=0)
Office_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='OfficeCode',index_col=0)

AreaUom_dict = AreaUom_df.to_dict()["DESCRIPTION"]
LengthUom_dict = LengthUom_df.to_dict()["DESCRIPTION"]
Office_dict = Office_df.to_dict()["DESCRIPTION"]
#domain name
domArea = "domAreaUom"
domLength = "domLengthUom"
domOffice = "domOfficeName"
#create domain
desc = arcpy.Describe(database)
domain = desc.domains
if domArea not in domain:
    # arcpy.DeleteDomain_management(database,domArea)
    print("Create Domain Area")
    arcpy.CreateDomain_management(database,domArea,"Area unit of name","TEXT","CODED")
    for code in AreaUom_dict:
        arcpy.AddCodedValueToDomain_management(database, domArea, code, AreaUom_dict[code])
        print("code added 1")
if domLength not in domain:
    # arcpy.DeleteDomain_management(database,domLength)
    print("Create Domain Length")
    arcpy.CreateDomain_management(database,domLength,"Length unit of name","TEXT","CODED")
    for code in LengthUom_dict:
        arcpy.AddCodedValueToDomain_management(database, domLength, code, LengthUom_dict[code])
        print("code added 2")
if domOffice not in domain:
    # arcpy.DeleteDomain_management(database,domOffice)
    print("Create Domain Office")
    arcpy.CreateDomain_management(database,domOffice,"SWCA Office name","TEXT","CODED")
    for code in Office_dict:
        arcpy.AddCodedValueToDomain_management(database, domOffice, code, Office_dict[code])
        print("code added 3")


    

def addDomain(fcList):
    for fc in fcList:
        fieldName = [f.name for f in arcpy.ListFields(fc)]
        if "projectOffice" in fieldName:
            arcpy.AssignDomainToField_management(fc, "projectOffice",domOffice)
        if "areaSizeUom" in fieldName:
            arcpy.AssignDomainToField_management(fc, "areaSizeUom",domArea)
        if "perimeterSizeUom" in fieldName:
            arcpy.AssignDomainToField_management(fc, "perimeterSizeUom",domLength)
        if "lengthSizeUom" in fieldName:
            arcpy.AssignDomainToField_management(fc, "lengthSizeUom",domLength)
        if "elevationUom" in fieldName:
            arcpy.AssignDomainToField_management(fc, "elevationUom",domLength)
        if "widthSizeUom" in fieldName:
            arcpy.AssignDomainToField_management(fc, "widthSizeUom",domLength)



print("Data Type: {}".format(dataType))
if dataType == "FeatureDataset":
    fcl = arcpy.ListFeatureClasses()
    if len(fcl) > 0:
        addDomain(fcl)
    else:
        print("Empty Dataset")


elif dataType == "Workspace":
    fcl = arcpy.ListFeatureClasses()
    if len(fcl) > 0:
        addDomain(fcl)
    else:
        pass

    datasets = arcpy.ListDatasets("*", "Feature")

    if len(datasets) > 0:
        for d in datasets:
            fcList = arcpy.ListFeatureClasses(feature_dataset = d)
            if len(fcList) > 0:
                addDomain(fcList)
            else:
                print("Dataset: {} is empty".format(d))



print("All done")
end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
print('Completed in {} minutes.'.format(ttl_time))

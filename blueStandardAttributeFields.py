"""
Author: Hitomi Nakamura
Date: 6/10/2020
Edit Date: 6/24/2020
Project Name:######
---Note---
This script will add all the required attribute fields from SWCA standard to the feature class.
Input can be gdb or dataset

"""

import arcpy
import time
import pandas as pd
start_time = time.time()
#input will be gdb or dataset
inputData = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True
arcpy.env.workspace = inputData

dataType = arcpy.Describe(inputData).dataType
if dataType == "FeatureDataset":
    database = arcpy.Describe(inputData).path
elif dataType == "Workspace":
    database = inputData

#create lists of required fields for polygon, line, and point
#obtain required fields list from the excel spreadsheet.
polygon_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='PolygonFeatureClass')#actual path needed
polygon_df = polygon_df.fillna("")
polygon_ls = polygon_df.values.tolist()
linear_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='LinearFeatureClass')
linear_df = linear_df.fillna("")
linear_ls = linear_df.values.tolist()
point_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='PointFeatureClass')
point_df = point_df.fillna("")
point_ls = point_df.values.tolist()



#create domain dictionaries for areaUom, lengthUom, projectOffice
#obtain the list from the excel spreadhseet and format into dictionary.
AreaUom_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='AreaUom',index_col=0)
LengthUom_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='LengthUom',index_col=0)
Office_df = pd.read_excel(r"SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='OfficeCode',index_col=0)

AreaUom_dict = AreaUom_df.to_dict()["DESCRIPTION"]
LengthUom_dict = LengthUom_df.to_dict()["DESCRIPTION"]
Office_dict = Office_df.to_dict()["DESCRIPTION"]

#domain name
domArea = "domAreaUom"
domLength = "domLengthUom"
domOffice = "domOfficeName"

####----create domain----####
desc = arcpy.Describe(database)
domain = desc.domains
if domArea not in domain:
    arcpy.AddMessage("Create Domain Area UOM")
    arcpy.CreateDomain_management(database,domArea,"Area unit of name","TEXT","CODED")
    for code in AreaUom_dict:
        arcpy.AddCodedValueToDomain_management(database, domArea, code, AreaUom_dict[code])
        

if domLength not in domain:
    arcpy.AddMessage("Create Domain Length UOM")
    arcpy.CreateDomain_management(database,domLength,"Length unit of name","TEXT","CODED")
    for code in LengthUom_dict:
        arcpy.AddCodedValueToDomain_management(database, domLength, code, LengthUom_dict[code])
        

if domOffice not in domain:
    arcpy.AddMessage("Create Domain Project Office")
    arcpy.CreateDomain_management(database,domOffice,"SWCA Office name","TEXT","CODED")
    for code in Office_dict:
        arcpy.AddCodedValueToDomain_management(database, domOffice, code, Office_dict[code])
        
    
#function that adds fields to the feature classes
def addFields(fcList):
    for fc in fcList:
        print(fc)
        if arcpy.Describe(fc).shapeType == "Polygon":
            dc = polygon_ls
        elif arcpy.Describe(fc).shapeType == "Polyline":
            dc = linear_ls
        elif arcpy.Describe(fc).shapeType == "Point":
            dc = point_ls

        fields = [f.name for f in arcpy.ListFields(fc)]
        fields = [f.upper() for f in fields]
        for d in dc:
            # print("d: {}".format(d))
            key = d[0]
            if key.upper() in fields:
                pass
            else:
                fieldName = d[0]
                fieldAlias = d[1]
                fieldType = d[2]
                if d[3] != "":
                    fieldLength = int(d[3])
                else:
                    fieldLength = d[3]

                arcpy.AddField_management(fc,fieldName,fieldType, "", "", fieldLength, fieldAlias)

#function that adds domain to the fields
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


###---if the input is feature dataset loop through the dataset to add all the required fields
### and associated domains to every feature classes---####
if dataType == "FeatureDataset":

    fcl = arcpy.ListFeatureClasses()
    if len(fcl) > 0:
        addFields(fcl)
        addDomain(fcl)
    else:
        pass
###---if the input is gdb, loop through the entire gdb including datasets to add all 
### the required fields and associated domains to every feature classes---####
elif dataType == "Workspace":
    fcl = arcpy.ListFeatureClasses()
    if len(fcl) > 0:
        addFields(fcl)
        addDomain(fcl)
    else:
        pass

    datasets = arcpy.ListDatasets("*", "Feature")

    if len(datasets) > 0:
        for d in datasets:
            fcList = arcpy.ListFeatureClasses(feature_dataset = d)
            if len(fcList) > 0:
                addFields(fcList)
                addDomain(fcList)
            else:
                arcpy.AddMessage("Dataset: {} is empty".format(d))


arcpy.AddMessage("All done")
end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
arcpy.AddMessage('Completed in {} minutes.'.format(ttl_time))

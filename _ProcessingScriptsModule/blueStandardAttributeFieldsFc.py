"""
Author: Hitomi Nakamura
Date: 7/2/2021
Edit Date: 
Project Name: Blue Standard
---Note---
This script will add all the required attribute fields from SWCA standard to the feature classes.
Input can be multiple feature classes.

"""

import arcpy
import time
import pandas as pd
start_time = time.time()
#input features can be multiple

def blueStandardAddField(fc,database):

    arcpy.env.overwriteOutput = True

    #domain dictionary
    AreaUom_df = pd.read_excel(r"N:\gisTools\Development\Python_Development_HitomiN\blueStandards\table\SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='AreaUom',index_col=0)
    LengthUom_df = pd.read_excel(r"N:\gisTools\Development\Python_Development_HitomiN\blueStandards\table\SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='LinearUom',index_col=0)
    Office_df = pd.read_excel(r"N:\gisTools\Development\Python_Development_HitomiN\blueStandards\table\SWCABlueStandardAttributeFields_forScript.xlsx",sheet_name='OfficeCode',index_col=0)

    AreaUom_dict = AreaUom_df.to_dict()["DESCRIPTION"]
    LengthUom_dict = LengthUom_df.to_dict()["DESCRIPTION"]
    Office_dict = Office_df.to_dict()["DESCRIPTION"]
    #domain name
    domArea = "domAreaUom"
    domLength = "domLinearUom"
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
            
    if domLength not in domain:
        # arcpy.DeleteDomain_management(database,domLength)
        print("Create Domain Length")
        arcpy.CreateDomain_management(database,domLength,"Length unit of name","TEXT","CODED")
        for code in LengthUom_dict:
            arcpy.AddCodedValueToDomain_management(database, domLength, code, LengthUom_dict[code])
            
    if domOffice not in domain:
        # arcpy.DeleteDomain_management(database,domOffice)
        print("Create Domain Office")
        arcpy.CreateDomain_management(database,domOffice,"SWCA Office name","TEXT","CODED")
        for code in Office_dict:
            arcpy.AddCodedValueToDomain_management(database, domOffice, code, Office_dict[code])
            


        

    def addDomain(fc):
        
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

    #access to spreadsheet for fields properties
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

    
    arcpy.AddMessage(fc)
    arcpy.AddMessage(arcpy.Describe(fc).shapeType)
    if arcpy.Describe(fc).shapeType == "Polygon":
        dc = polygon_ls
        
    elif arcpy.Describe(fc).shapeType == "Polyline":
        dc = linear_ls
        
    elif arcpy.Describe(fc).shapeType == "Point" or arcpy.Describe(fc).shapeType == "Multipoint":
        dc = point_ls
        
    
    fields = [f.name for f in arcpy.ListFields(fc)]
    fields = [f.lower() for f in fields]
    # arcpy.AddMessage("fields {}".format(fields))
    for d in dc:
        # print("d: {}".format(d))
        key = d[0].replace(' ','')
        # arcpy.AddMessage("key {}".format(key.upper()))
        if key.lower() in fields:
            pass
        else:
            # arcpy.AddMessage("key {}".format(key.upper()))
            fieldName = d[0]
            fieldAlias = d[1]
            fieldType = d[2]
            if d[3] != "":
                fieldLength = int(d[3])
            else:
                fieldLength = d[3]

            arcpy.AddField_management(fc,fieldName,fieldType, "", "", fieldLength, fieldAlias)

    addDomain(fc)

    return fc


if __name__ == '__main__':
    print("running directly")


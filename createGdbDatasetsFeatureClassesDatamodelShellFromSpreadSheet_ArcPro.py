"""
Author: Hitomi Nakamura
Date: 4/2/2020

Project Name: Standard
---Note---
This script will create GDB, Datasets and Feature classes from spreadsheet. It will also create spreadsheet shell for individual feature class in user specified location

"""

import arcpy
import time
import pandas as pd
import sys
import os
start_time = time.time()

spreadsheet = arcpy.GetParameterAsText(0)
outSpreadsheetLocation = arcpy.GetParameterAsText(1)


sheetLists = pd.read_excel(spreadsheet,sheet_name=None).keys()

try:
    # if "GDB" in sheetLists:
    gdb_df = pd.read_excel(spreadsheet,sheet_name='GDB')
    
except :
    raise ValueError(f"'GDB' sheet does not exist in {spreadsheet}")

try:
    # if "Dataset" in sheetLists:
    dataset_df = pd.read_excel(spreadsheet,sheet_name='Dataset')
    
except:
    raise ValueError(f"'Dataset' sheet does not exist in {spreadsheet}")
    
try:
    # if "Feature Class" in sheetList:
    fc_df = pd.read_excel(spreadsheet,sheet_name='Feature Class')
    
except:
    raise ValueError(f"'Feature Class' sheet does not exist in {spreadsheet}")
    
gdb_list = gdb_df.values.tolist()
dataset_list = dataset_df.values.tolist()
fc_df = fc_df.fillna("")
fc_list = fc_df.values.tolist()

arcpy.env.overwriteOutput = True
###----Create FGDB----####
for gdb in gdb_list:
    gdbLocation = gdb[0]
    gdbName = gdb[1]
    gdbFullPath = os.path.join(gdbLocation,gdbName)
    if arcpy.Exists(gdbFullPath):
        pass
    else:
        arcpy.CreateFileGDB_management(gdbLocation,gdbName)
###----Create Datasets----####
for dataset in dataset_list:
    datasetName = dataset[0]
    coordinateSystem = dataset[1]
    if type(coordinateSystem)==str:
        
        coordinateSystem = coordinateSystem.replace("_"," ")
    try:
        sr = arcpy.SpatialReference(coordinateSystem)
    except:
        raise ValueError(f"{coordinateSystem} is not a valid input. Please update the spreadsheet. Refer https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/spatialreference.htm for more info.")
        
    
    arcpy.env.workspace = gdbFullPath
    datasetsInGDB = arcpy.ListDatasets()
    if datasetName not in datasetsInGDB:
        arcpy.CreateFeatureDataset_management(gdbFullPath,datasetName,sr)
    else:
        pass

###----Create feature classes and spreadsheet shell----###
datasetInGDB = arcpy.ListDatasets()
for fc in fc_list:
    datasetToAdd = fc[0]
    featureClassName = fc[1]
    if datasetToAdd != "":
        outFc = f"{datasetToAdd}\\{featureClassName}"
        if datasetToAdd not in datasetInGDB:
            raise Exception(f"{datasetToAdd} not in {gdbFullPath}. Please add the {datasetToAdd} to Dataset sheet and rerun it.")
            
    else:
        outFc = featureClassName
    fcCoordinateSystem = fc[2]
    geometryType = fc[3].upper()

    if geometryType in ['POINT','PT','POINTS']:
        geometryType = 'POINT'
    elif geometryType in ['MULTIPOINT','MULTIPT','MULTI-POINT','MULTIPOINTS']:
        geometryType = 'MULTIPOINT'
    elif geometryType in ['LINE','POLYLINE','LINES','LN']:
        geometryType = 'POLYLINE'
    elif geometryType in ['POLYGON','PY','POLYGONS']:
        geometryType = 'POLYGON'
    else:
        raise Exception(f"{geometryType} is an invalid value. Please fill the Geometry Type column with 'Point','Polyline','Polygon' or 'Multipoint'")
        

    
    
    if arcpy.Exists(outFc):
        fcDataType = arcpy.Describe(outFc).dataType
        if geometryType == fcDataType.upper():
            print(f"{outFc} already exists.")
        else:
            raise Exception(f"{outFc} already exists but does not match the geometry type in the spreadsheet.")
            
    else:
        try:
            sr = arcpy.SpatialReference(coordinateSystem)
        except:
            raise ValueError(f"{coordinateSystem} is not a valid input. Please update the spreadsheet. Refer https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/spatialreference.htm for more info.")
            

        try:
            outpath = os.path.join(gdbFullPath,datasetToAdd)
            arcpy.CreateFeatureclass_management(outpath,featureClassName,geometryType,"","","",sr)
        except arcpy.ExecuteError:
            arcpy.AddError(arcpy.GetMessages(2))
            print(arcpy.GetMessages(2))
        
        #create df for feature class
        masterSheetName = "Master"
        masterData = {'Feature Class Location':[f"{outpath}\\{featureClassName}"],'Coordinate System':[fcCoordinateSystem],'Geometry Type':[geometryType]}
        masterSheet_df = pd.DataFrame(data=masterData)
        fcSheetName = f"{geometryType}FeatureClass"
        fcSheet_df = pd.DataFrame(columns = ['Attribute Name','Alias','Data Type','Field Length','Domain Table'])
        domainSheetName = "Domain"
        domainSheet_df = pd.DataFrame(columns = ['Domain Name','Domain Description','Type'])
        outputxlsx = f"{outSpreadsheetLocation}\\{featureClassName}.xlsx"
        with pd.ExcelWriter(outputxlsx) as writer:
            masterSheet_df.to_excel(writer,sheet_name=masterSheetName,index=False)
            fcSheet_df.to_excel(writer,sheet_name=fcSheetName,index=False)
            domainSheet_df.to_excel(writer,sheet_name=domainSheetName,index=False)


end_time = time.time()
ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
arcpy.AddMessage('Completed in {} minutes.'.format(ttl_time))
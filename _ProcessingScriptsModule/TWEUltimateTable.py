import arcpy
import pandas as pd
import os
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from functools import reduce
import numpy as np

def DataFrame(fieldOffice):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"N:\Projects\test.gdb"
    gdb = r"N:\Projects\anothertest.gdb"
    boreholeOrigin = r"N:\Projects\test.sde\Infrastructure\Prelim_Geotech_Points"
    borehole = "borehole"
    arcpy.MakeFeatureLayer_management(boreholeOrigin,borehole,where_clause="status = 'Active'")
    accessRoad = r'N:\Projects\anothertest.gdb\infrastructure\GeotechBoreAccessRoadsBLMFO'
    noxiousWeeds = r"N:\Projects\anothertest.gdb\sssPlants\NoxiousWeeds"
    masterTablePath = r"N:\Projects\test.xlsx"

    requirementMergeLayer = 'memory/requirementMergeLayer'
    fieldOffice_ = fieldOffice.replace(' ','_')

    mergingList = []
    #create merge layer from requirementId table
    requirementTable = pd.read_excel(masterTablePath,sheet_name='All Geotech')
    requirementList = requirementTable.values.tolist()
    for req in requirementList:
        dataset = req[4]
        fc = req[5]
        fcPath = os.path.join(gdb,dataset,fc)
        if arcpy.Exists(fcPath):
            mergingList.append(fcPath)
    arcpy.Merge_management(mergingList,requirementMergeLayer)
    #Select borehole based on field offices
    boreholeTable = pd.read_excel(masterTablePath,sheet_name='Borehole')
    foBoreholeTable = boreholeTable[boreholeTable["Field Office"]==fieldOffice]
    foBoreholeTable.update("'"+foBoreholeTable['Bore Name'].astype(str)+"'")
    boreId = ",".join(foBoreholeTable['Bore Name'].values.tolist())
    sql = f"name IN ({boreId})"
    boreIdSelect = f"{fieldOffice_}_boreIdSelect"
    arcpy.MakeFeatureLayer_management(borehole,boreIdSelect,where_clause=sql)
    #intersect bore location with requirement
    boreholeReqIntersect = f'memory/{fieldOffice_}_boreholeReqIntersect'
    arcpy.Intersect_analysis([boreIdSelect,requirementMergeLayer],boreholeReqIntersect)
    
    #intersect access road with requirement
    foAccessRoad = f'{fieldOffice_}_AccessRoad'
    accessSql = f"label LIKE '{fieldOffice}%'"
    arcpy.MakeFeatureLayer_management(accessRoad,foAccessRoad,where_clause=accessSql)
    foAccessReqIntersect = f'memory/{fieldOffice_}_AccessRequirementIntersect'
    arcpy.Intersect_analysis([foAccessRoad,requirementMergeLayer],foAccessReqIntersect)

    #intersect with noxious weeds

    #intersect with bore location
    boreholeNoxIntersect = f'memory/{fieldOffice_}_boreholeNoxIntersect'
    arcpy.Intersect_analysis([boreIdSelect,noxiousWeeds],boreholeNoxIntersect)
    #intersect with access road
    accessNoxIntersect = f'memory/{fieldOffice_}_accessNoxIntersect'
    arcpy.Intersect_analysis([foAccessRoad,noxiousWeeds],accessNoxIntersect)
    
    #create dataframe and drop duplicates
    boreholeNoxIntersectDf = pd.DataFrame.spatial.from_featureclass(boreholeNoxIntersect)
    accessNoxIntersectDf = pd.DataFrame.spatial.from_featureclass(accessNoxIntersect)
    noxIntersectDf = pd.concat([boreholeNoxIntersectDf,accessNoxIntersectDf.rename(columns={'BoreName':'name'})],ignore_index=True)
    noxIntersectDf = noxIntersectDf.drop_duplicates(subset=['common_name','name'],keep='last')


    #create dataframe with additional information of requirements
    boreholeReqIntersectDf = pd.DataFrame.spatial.from_featureclass(boreholeReqIntersect)
    boreholeReqIntersectWithInfoDf = pd.merge(boreholeReqIntersectDf[["req_num","name"]],requirementTable,how="left",left_on="req_num",right_on="req_num In output field")
    #access road with info
    accessReqIntersectDf = pd.DataFrame.spatial.from_featureclass(foAccessReqIntersect)
    accessReqIntersectWithInfoDf = pd.merge(accessReqIntersectDf[["BoreName","req_num"]],requirementTable,how="left",left_on="req_num",right_on="req_num In output field")
    
    #merge boring location dataframe and access road dataframe
    df = pd.concat([boreholeReqIntersectWithInfoDf,accessReqIntersectWithInfoDf.rename(columns={'BoreName':'name'})],ignore_index=True)
    df = df.drop_duplicates(subset=['req_num','name'],keep='last')
    #intersect with landownership
    landOwnership = 'https://featureserviceURL'
    boreholeLandOwnership = 'memory/boreholeLandownershipIntersect'
    arcpy.Intersect_analysis([borehole,landOwnership],boreholeLandOwnership)

    boreholelandOwnershipDf = pd.DataFrame.spatial.from_featureclass(boreholeLandOwnership)
    boreholelandOwnershipDf.loc[boreholelandOwnershipDf['fieldoffice']=='Southern Nevada Field Office','fieldoffice']='Las Vegas Field Office'

    tableList = []
    foTable = pd.read_excel(masterTablePath,sheet_name=fieldOffice)
    columnNames = foTable['Column Name'].unique()

    columnNameList = columnNames.tolist()

    for columnName in columnNames:
            
        subDf = foTable[foTable['Column Name']==columnName]
        boreholeReqSelectDf = pd.merge(df[['req_num','name','Timing']],subDf,how = 'inner',left_on='req_num',right_on='req_num In output field')
        boreholeReqSelectDf=boreholeReqSelectDf.filter(['name','req_num','Timing','Column Name'])
        
        foBoreholeAccessTable = boreholeTable[boreholeTable["Field Office"]==fieldOffice]
        foBoreholeAccessTable.rename(columns={'Bore Name':'name'},inplace=True)
        # print(foBoreholeAccessTable)
        if columnName == 'Raptor Seasonal Stip':
            boreholeReqSelectDf['Timing']=boreholeReqSelectDf['Timing'].astype(str)
            boreholeReqSelectDf = boreholeReqSelectDf.groupby('name')['Timing'].apply(', '.join).reset_index()
        else:
            boreholeReqSelectDf = boreholeReqSelectDf.groupby('name')['req_num'].apply(', '.join).reset_index()
        
        foBoreholeDf = boreholelandOwnershipDf[boreholelandOwnershipDf['fieldoffice']==f"{fieldOffice} Field Office"]
        
        joinDf = pd.merge(foBoreholeDf['name'],boreholeReqSelectDf,how='left',left_on='name',right_on = 'name')
        
        if columnName == 'Raptor Seasonal Stip':
            joinDf.rename(columns={'Timing':columnName},inplace=True)
        else:
            joinDf.rename(columns={'req_num':columnName},inplace=True)
        tableList.append(joinDf)
    foBoreholeDf = pd.merge(foBoreholeAccessTable[['name','Field Office','Access Road ID']],foBoreholeDf,how ='left',left_on='name',right_on='name')
    
    tableList.append(foBoreholeDf)
    # tableList.append(foBoreholeAccessTable)
    allColumnList = ['name']+['Access Road ID']+['Field Office']+['acm_owner']+columnNameList

    noxDf = noxIntersectDf.groupby('name')['common_name'].apply(', '.join).reset_index()
    noxDf.rename(columns={'common_name':'Noxious Weeds'},inplace=True)
    tableList.append(noxDf)
    allColumnList += ['Noxious Weeds']


    fullDf = reduce(lambda left,right:pd.merge(left,right,on='name',how='outer'),tableList)

    fullDf = fullDf[allColumnList]
    fullDf.rename(columns={'name':'Boring ID','acm_owner':'Land Ownership (Borehole Only)'},inplace=True)
    
    #calculate earliest drill date and latest drill date
    earliestDrillDate = 'Earliest Drill Date (2021)'
    latestDrillDate = 'Latest Drill Date (2021)'
    earliestRaptor = 'Raptor Early'
    subTable = foTable[['Column Name','Earliest Column Value','New Column Name','Latest Drill Date']]
    subTable = subTable.loc[subTable['Earliest Column Value'].notnull()]
    subTable = subTable.drop_duplicates(subset=['Earliest Column Value','New Column Name'])
    otherTimingList = subTable.values.tolist()

    latestTimingDf = subTable.loc[subTable['Latest Drill Date'].notnull()]

    latestTimingDf = latestTimingDf.drop_duplicates(subset=['Latest Drill Date'])
    latestTimingList = latestTimingDf.values.tolist()
    # selectDf = fullDf.dropna(subset=timingColumnNameList,how='all')
    selectDf = fullDf.fillna('')

    #Raptor Timing Earliest
    selectDf[earliestRaptor] = selectDf['Raptor Seasonal Stip'].str.split(',| - |-').str[1::2].apply(sorted).str[-1]
    #other timing Earliest
    
    columnAppendList = []
    for l in otherTimingList:
        columnName = l[0]
        columnValue = l[1]
        newColumn = l[2]
        selectDf[newColumn]=np.where((selectDf[columnName]!=""),columnValue,"")
        columnAppendList.append(newColumn)
    columnAppendList.append(earliestRaptor)
    
    selectDf[earliestRaptor]=selectDf[earliestRaptor].fillna("")
    selectDf[earliestDrillDate]=selectDf[columnAppendList].max(axis=1)
    selectDf = selectDf.loc[(selectDf[earliestDrillDate]!="")]
    selectDf[earliestDrillDate]=pd.to_datetime(selectDf[earliestDrillDate],format="%m/%d")+pd.DateOffset(days=1)
    selectDf[earliestDrillDate]=selectDf[earliestDrillDate].dt.strftime('%m/%d')

    #other timing latest
    if latestTimingDf.shape[0]!=0:
        for l in latestTimingList:
            columnName = l[0]
            columnValue = l[3]
            selectDf[latestDrillDate]=np.where((selectDf[columnName]!=""),columnValue,"12/31")
    else:
        selectDf[latestDrillDate]='12/31'
    
    selectDf = selectDf[['Boring ID',earliestDrillDate,latestDrillDate]]
    selectDf.rename(columns={'Boring ID':'boringID'},inplace=True)
    

    #merge earliest and latest drill columns with main df

    finalDf = fullDf.merge(selectDf,how='left',left_on='Boring ID',right_on='boringID')
    finalDf = finalDf.drop(['boringID'],axis=1)
    return finalDf


if __name__ == '__main__':

    print("running directly")
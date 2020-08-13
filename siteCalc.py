import arcpy
import time
# Track script execution time

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"N:\GIS_Tools\_RMPNW\CR_Site_Calcs_H\outWorkspace.gdb"

fcs = arcpy.ListFeatureClasses()
if len(fcs) > 0:
    for fc in fcs:
        arcpy.Delete_management(fc)
else:
    pass

tbls = arcpy.ListTables()
if len(tbls) > 0:
    for tbl in tbls:
        arcpy.Delete_management(tbl)
else:
    pass
#input1
in_fc = arcpy.GetParameterAsText(0) 
#input2
dem =  arcpy.GetParameterAsText(1)
#input3
# plssFirstDiv = arcpy.GetParameterAsText(2)
#input4
# plssSecondDiv = arcpy.GetParameterAsText(3)
#input5
outLocationCsv = arcpy.GetParameterAsText(2)
#input6
utmCoordinate = arcpy.GetParameterAsText(3)
#input7
utmCoordinateCsv = arcpy.GetParameterAsText(4)

#make gdb and store UTM, USGS 24k topo usa
plssFirstDiv = 'N:\\GIS_Tools\\_RMPNW\\CR_Site_Calcs_H\\plss.gdb\\PLSSFirstDivision'
plssSecondDiv = 'N:\\GIS_Tools\\_RMPNW\\CR_Site_Calcs_H\\plss.gdb\\PLSSSecondDivision'
utm = 'N:\\GIS_Tools\\_RMPNW\\CR_Site_Calcs_H\\CalcSiteDatabase.gdb\\utmzone_dissolve'
quad = 'N:\\GIS_Tools\\_RMPNW\\CR_Site_Calcs_H\\CalcSiteDatabase.gdb\\USGS_24k_Topo_USA'



def SJ(inFeature, joinFeature, outName):
    arcpy.SpatialJoin_analysis(inFeature, joinFeature, outName, 'JOIN_ONE_TO_MANY','KEEP_COMMON','','INTERSECT')
    return outName

def elevation(inFeature, outName):
    point = arcpy.FeatureToPoint_management(inFeature, outName, 'INSIDE')
    arcpy.AddSurfaceInformation_3d(point, dem, "Z")
    ftPoint = 'z_ft'
    point_fields = arcpy.ListFields(point, ftPoint)
    if len(point_fields) != 1:
        arcpy.AddField_management(point, ftPoint, "DOUBLE")
    else:
        pass
    arcpy.CalculateField_management(point, ftPoint, '!Z! * 3.28084', 'PYTHON3')
    return point

def addField(inFeature, inList, f_type):
    for l in inList:
        fields = arcpy.ListFields(inFeature, l)
        if len(fields) != 1:
            arcpy.AddField_management(inFeature, l, f_type)
        else:
            pass
    return inFeature
def deleteFields(feature, reqList):
    reqList = set(reqList)
    delList = []
    listFields = arcpy.ListFields(feature)
    for f in listFields:
        if f.required or f.name in reqList:
            pass
        else:
            delList.append(f.name)
    if len(delList) > 0:
        return arcpy.DeleteField_management(feature, delList)
    else:
        return feature

def reverseDeleteField(inFeature,key):
    key = set(key)
    delList = []
    ls = arcpy.ListFields(inFeature)
    for l in ls:
        if not l.required:
            for k in key:
                if k.upper() in l.name.upper():
                    delList.append(l.name)
                else:
                    pass
    if len(delList) > 0:
        return arcpy.DeleteField_management(inFeature, delList)
    else:
        return inFeature

try:

    #join utm and input feature
    utmJoin = 'site_utm'
    if arcpy.Exists(utmJoin) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(utmJoin)
    SJ(in_fc, utm,utmJoin)

    #add area attribute to feature
    #meter

    areas = ['area_meter','acres']
    # for area in areas:
    #     area_fields = arcpy.ListFields(utmJoin, area)
    #     if len(area_fields) != 1:
    #         arcpy.AddField_management(utmJoin, area,"DOUBLE")
    #     else:
    #         pass
    addField(utmJoin, areas, "DOUBLE")
    arcpy.CalculateField_management(utmJoin, areas[0], '!Shape!.getArea("GEODESIC","SQUAREMETERS")', 'PYTHON3')
    arcpy.CalculateField_management(utmJoin, areas[1], '!Shape!.getArea("GEODESIC","ACRES")', 'PYTHON3')

    #delete unnecessary attributes in utmJoin
    reqUTM = ['ZONE','TARGET_FID','area_meter','acres']
    deleteFields(utmJoin, reqUTM)


    zPoint = 'zPoint'
    if arcpy.Exists(zPoint) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(zPoint)
    elevation(in_fc, zPoint)
    centroid = ['cent_x','cent_y']
    addField(zPoint,centroid,"DOUBLE")

    arcpy.CalculateGeometryAttributes_management(zPoint,[[centroid[0],'POINT_X'],[centroid[1],'POINT_Y']])
    # arcpy.CalculateGeometryAttributes_management(zPoint,[['cent_x','POINT_X'],['cent_y','POINT_Y']])
    
    #delete unnecessary attributes in zPoint
    reqZ = ['z_ft','ORIG_FID','cent_x','cent_y']
    deleteFields(zPoint, reqZ)

    #create minimum bounding geometry in convex hull
    convex = 'site_convex'
    if arcpy.Exists(convex) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(convex)   
    arcpy.MinimumBoundingGeometry_management(in_fc, convex, 'CONVEX_HULL', 'NONE', '', 'MBG_FIELDS')

    #add width and length in Ft
    ft = ['width_ft','length_ft']
    addField(convex,ft, "DOUBLE")

    arcpy.CalculateField_management(convex, ft[0], '!MBG_Width! * 3.28084', 'PYTHON3')
    arcpy.CalculateField_management(convex, ft[1], '!MBG_Length! * 3.28084', 'PYTHON3')

    #delete unnecessary attributes in convex
    reqConvex = ['ORIG_FID','MBG_Width','MBG_Length', 'width_ft','length_ft']
    deleteFields(convex, reqConvex)

    #create minimum bounding geometry in envelope
    # envelope = 'site_envelope'
    # if arcpy.Exists(envelope) and arcpy.env.overwriteOutput:
    #     arcpy.Delete_management(envelope)
    # arcpy.MinimumBoundingGeometry_management(in_fc, envelope, 'ENVELOPE', 'NONE','','NO_MBG_FIELDS')
    # #new attribute columns
    # coordinate = ['min_x','min_y','max_x','max_y']

    # addField(envelope, coordinate, "DOUBLE")
    # for c in coordinate:
    #     c_fields = arcpy.ListFields(envelope, c)
    #     if len(c_fields) != 1:
    #         arcpy.AddField_management(envelope,c,"DOUBLE")
    #     else:
    #         pass

    # arcpy.CalculateGeometryAttributes_management(envelope, [['min_x', 'EXTENT_MIN_X'],
    #                                                     ['min_y', 'EXTENT_MIN_Y'],
    #                                                     ['max_x', 'EXTENT_MAX_X'],
    #                                                     ['max_y','EXTENT_MAX_Y']])

    #delete attributes
    # reqEnvelope = ['min_x','min_y','max_x','max_y','ORIG_FID']
    # deleteFields(envelope, reqEnvelope)


    #join utm, z, convex (width and height), envelope (min/max coordinates)
    inLayer = 'inLayer'
    if arcpy.Exists(inLayer) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(inLayer)
    arcpy.MakeFeatureLayer_management(in_fc, inLayer)
    arcpy.AddJoin_management(inLayer, 'OBJECTID', utmJoin, 'TARGET_FID')
    arcpy.AddJoin_management(inLayer, 'OBJECTID', zPoint, 'ORIG_FID')
    arcpy.AddJoin_management(inLayer, 'OBJECTID', convex, 'ORIG_FID')
    # arcpy.AddJoin_management(inLayer, 'OBJECTID', envelope, 'ORIG_FID')
    fc_joined = 'fc_joined'
    if arcpy.Exists(fc_joined) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(fc_joined)
    arcpy.CopyFeatures_management(inLayer, fc_joined)

    # arcpy.RemoveJoin_management(inLayer, utmJoin)

    #remove unnecessary attributes from fc_joined
    keyWords = ['OBJECTID','ORIG_FID','Shape']
    reverseDeleteField(fc_joined, keyWords)


    # keywords = set(keyWords)
    # delList = []
    # listFields = arcpy.ListFields(fc_joined)
    # for f in listFields:
    #     if not f.required:
    #         for key in keyWords:
    #             if key in f.name:
    #                 delList.append(f.name)
    #             else:
    #                 pass
    # if len(delList) > 0:
    #     arcpy.DeleteField_management(fc_joined, delList)




    # quadLayer = 'quadLayer'
    # if arcpy.Exists(quadLayer) and arcpy.env.overwriteOutput:
    #     arcpy.Delete_management(quadLayer)
    # arcpy.MakeFeatureLayer_management(quad,quadLayer)

    reqQuad = ['QUAD_NAME','ST_NAME1','Date', 'Label']
    deleteFields(quad, reqQuad)

    fc_quad = 'fc_quad'
    if arcpy.Exists(fc_quad) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(fc_quad)
    SJ(fc_joined, quad, fc_quad)

    #plssFirstDiv
    fc_quad_firstDiv = 'fc_quad_firstDiv'
    if arcpy.Exists(fc_quad_firstDiv) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(fc_quad_firstDiv)
    SJ(fc_quad, plssFirstDiv, fc_quad_firstDiv)

    #add fields to plss
    plssFirstDiv_a = ['State','Primer','Town','Twndir','range','rngdir','section']  #'qq']
    addField(fc_quad_firstDiv, plssFirstDiv_a, "TEXT")


    arcpy.CalculateField_management(fc_quad_firstDiv, 'State', '!FRSTDIVID![0:2]', 'PYTHON3')
    arcpy.CalculateField_management(fc_quad_firstDiv, 'Primer', '!FRSTDIVID![2:4]', 'PYTHON3')
    arcpy.CalculateField_management(fc_quad_firstDiv, 'Town', '!FRSTDIVID![4:7]', 'PYTHON3')
    # arcpy.CalculateField_management(fc_quad_firstDiv, 'Twnfrt', '!FRSTDIVID![7:8]', 'PYTHON3')
    arcpy.CalculateField_management(fc_quad_firstDiv, 'Twndir', '!FRSTDIVID![8:9]', 'PYTHON3')
    arcpy.CalculateField_management(fc_quad_firstDiv, 'range', '!FRSTDIVID![9:12]', 'PYTHON3')
    
    #range dir
    arcpy.CalculateField_management(fc_quad_firstDiv, 'rngdir', '!FRSTDIVID![13:14]', 'PYTHON3')
    arcpy.CalculateField_management(fc_quad_firstDiv, 'section', '!FRSTDIVID![17:19]', 'PYTHON3')


    # reqPlss = ['State','Primer','Town','Twnfrt','Twndir','range','rngfrt','section','qq','SECDIVID']
    # deleteFields(plssLayer, reqPlss)

    #join second division and populate qq
    fc_quad_plss = 'fc_quad_plss'
    if arcpy.Exists(fc_quad_plss) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(fc_quad_plss)
    SJ(fc_quad_firstDiv, plssSecondDiv, fc_quad_plss)

    plssSecondDiv_a = ['qq']
    addField(fc_quad_plss, plssSecondDiv_a, "TEXT")

    # arcpy.CalculateField_management(fc_quad_plss, 'qq', '!SECDIVID![20:]', 'PYTHON3')
    # arcpy.CalculateField_management(fc_quad_plss, 'qq', expression, 'PYTHON3', codeBlock)
    expression = 'qqCalc(!SECDIVID![20:])'
    codeBlock = """def qqCalc(qq):
        if qq[0:1] == 'A':
            qq = qq[1:]
            return qq
        else:
            return qq"""

    arcpy.CalculateField_management(fc_quad_plss, 'qq', expression, 'PYTHON3', codeBlock)

    finalKeyWords = ['OBJECTID','ORIG_FID','Shape','Join','TARGET_FID','FRSTDIV','SECDIV']
    reverseDeleteField(fc_quad_plss,finalKeyWords)
    #create csv file
    arcpy.CopyRows_management(fc_quad_plss, outLocationCsv)


    #steps to create utm coordinate spreadsheet and point feature
    point = 'polygon_to_vertices'
    arcpy.FeatureVerticesToPoints_management(in_fc, point, "ALL")

    inList = ['x','y']
    addField(point, inList, "DOUBLE")

    arcpy.CalculateGeometryAttributes_management(point, [['x', 'POINT_X'],['y', 'POINT_Y']])

    ls = []
    with arcpy.da.SearchCursor(point, 'ORIG_FID') as cursor:
        for row in cursor:
            ORIGID = row[0]
            if row[0] not in ls:
                ls.append(row[0])
            else:
                pass
    # print(ls)
    count_OID = len(ls) #30

    #empty dictionary
    d= {}
    for l in ls:
        d[l]={}
        d[l]['x'] = {}
        d[l]['y'] = {}
    # print(d)

    updateField = ['OBJECTID','ORIG_FID','x','y']
    i = 0


    with arcpy.da.SearchCursor(point, updateField) as cursor:
        for row in cursor:
            orig_id = row[1]
            oid = row[0]
            d[orig_id]['x'][oid] = row[2]
            d[orig_id]['y'][oid] = row[3]

    oidLs = []

    def oidSelect(d):
        for k, v in d.items():
            # print("{} : {}".format(k,v))
            for kk, vv in v.items():
                # print("second * {} : {}".format(kk,vv))
                min_c = min(vv, key=vv.get)
                max_c = max(vv, key=vv.get)
                min_c_append = '"OBJECTID" = {} OR '.format(min_c)
                max_c_append = '"OBJECTID" = {} OR '.format(max_c)
                oidLs.append(min_c_append)
                oidLs.append(max_c_append)

        return oidLs

    oidSelect(d)

    sql = "".join(oidLs)
    sql = sql[:-4]

    arcpy.MakeFeatureLayer_management(point,"point_lyr")
    arcpy.SelectLayerByAttribute_management("point_lyr", 'NEW_SELECTION', sql)
    arcpy.CopyFeatures_management("point_lyr", utmCoordinate)
    arcpy.CopyRows_management("point_lyr", utmCoordinateCsv)

    print('done with calculations')


except ShapeError as err:
    print(err[0])
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
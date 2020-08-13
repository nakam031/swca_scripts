import os
import arcpy
from arcpy.sa import *
from arcpy.ia import *

arcpy.env.workspace = input("Path to the work space: ") #"C:/Users/hitomi.nakamura/Documents/viewshed_volume/data/viewshed_calc.gdb"   #
arcpy.env.overwriteOutput = True
env = arcpy.env.workspace
# arcpy.checkOutExtension("Spatial")

#input
point = input("Point feature name: ") #"Ekola_800mPoints_20191113" 
#input for basename
baseName = input("Basename: ") #'EK_'  
#input for dem
dem = input("DEM name: ")   #'EK_DEM' 


desc = arcpy.Describe(point)
spr = desc.spatialReference
pC = input("EPSG Project Coordinate: ")
vC = input("EPSG Vertical Coordinate: ")  #5703
radius_buffer = input("Buffer radius in meter: ") #800
height =  input("Height of the ceiling in meter: ") #200
uID = input("Name or unique ID field name of the point feature (eg. IDENT): ")
tablePath = input("Output csv file saving location: ")
tableName = input("Output csv file name with extention: ")
outTable = os.path.join(tablePath, tableName)


#buffer function
def buffer(point, outName, meter):
    if arcpy.Exists(outName) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(outName)
    return arcpy.Buffer_analysis(point, outName, meter)

#extract by mask function
def clipRaster(dem, bufferName, outName):
    if arcpy.Exists(outName) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(outName)
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(int(pC), int(vC))
    outExtractByMask = ExtractByMask(dem, bufferName)
    return outExtractByMask.save(outName)

#plus function
def plus(dem, ceiling_height, outName):
    if arcpy.Exists(outName) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(outName)
    outPlus = Plus(dem, ceiling_height)
    outPlus.save(outName)

#create skyline multipatch function
def skyline(dem_cover_base,observer_point, bufferMeter1):
    outName = 'skyline_' + str(radius_buffer)
    surfaceRadius = '1000 meters'
    surfaceElevation = '0 meters'
    inFeatures = ''
    levelOfDetail = 'FULL_DETAIL'
    fromAzim = 0
    toAzim = 360
    incAzim = 1
    maxHorizonRadius = bufferMeter1
    segSky = 'NO_SEGMENT_SKYLINE'
    scale = 100
    scaleAccordingTo = 'VERTICAL_ANGLE'
    scaleMethod = 'SKYLINE_MAXIMUM'
    useCurvature = 'NO_CURVATURE'
    
    #if feature class exists, delete them
    if arcpy.Exists(outName) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(outName)
    #run skyline tool
    return arcpy.Skyline_3d(observer_point, outName, dem_cover_base, surfaceRadius, 
                     surfaceElevation, inFeatures, levelOfDetail, fromAzim, toAzim, incAzim, maxHorizonRadius,
                    segSky, scale, scaleAccordingTo, scaleMethod, useCurvature)
    
#run skyline barrier tool
def skylineBarrier(observer_point, skyline, outName, minRadius, maxRadius):
    if arcpy.Exists(outName) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(outName)
    return arcpy.SkylineBarrier_3d(observer_point, skyline, outName, minRadius, maxRadius, 'CLOSED')


    
def multipatchToRaster(multipatch, outName):
    if arcpy.Exists(outName) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(outName)
    return arcpy.MultipatchToRaster_conversion(multipatch, outName, cellSize)

#calculate the difference
def cutFill(beforeRas, afterRas, outName):
    if arcpy.Exists(outName) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(outName)
    outCutFill = CutFill(beforeRas, afterRas, 1)
    return outCutFill.save(outName)  

#create polygon from cutfill rasters

def rasterToPolygon(inRaster, outName):
    if arcpy.Exists(outName) and arcpy.env.overwriteOutput:
        arcpy.Delete_management(outName)
    field = 'VALUE'
    arcpy.RasterToPolygon_conversion(inRaster, outName, "NO_SIMPLIFY", field)


######STEPS######

try:
    # step 1 add surface information from DEM
    if desc.shapeType == 'Point':
        arcpy.AddSurfaceInformation_3d(point, dem, "Z","BILINEAR")



        # step 2 add column for height
        height_field = "p_height"
        point_fields = arcpy.ListFields(point, height_field)
        if len(point_fields) != 1:
            arcpy.AddField_management(point, height_field, "DOUBLE")
        else:
            pass

        # populate person_height field (THIS COULD BE A function)
        arcpy.CalculateField_management(point,height_field, '!Z! + 1.8288', 'PYTHON3')

        #create 6ft+ point
        point_6ft_name = 'point_6ft'
        if arcpy.Exists(point_6ft_name) and arcpy.env.overwriteOutput:
            arcpy.Delete_management(point_6ft_name)
        arcpy.FeatureTo3DByAttribute_3d(point, point_6ft_name, height_field)



        ####create buffers

        bufferName_1 = baseName + 'buffer_' + str(radius_buffer)
        bufferMeter1 = str(radius_buffer) + ' Meter'

        buffer2 = int(radius_buffer) + 200
        bufferName_2 = baseName + 'buffer_' + str(buffer2)
        bufferMeter2 = str(buffer2) + ' Meter'

        buffer3 = int(radius_buffer) + 50
        bufferName_3 = baseName + 'buffer_' + str(buffer3)
        bufferMeter3 = str(buffer3) + ' Meter'


        ####execute buffers
        buffer(point, bufferName_1, bufferMeter1)
        buffer(point, bufferName_2, bufferMeter2)
        buffer(point, bufferName_3, bufferMeter3)



        ####execute extract by mask function
        dem_cover_base = baseName + 'dem' + str(buffer2) + 'B'

        clipRaster(dem, bufferName_2, dem_cover_base)


            
        #plus 200m height, execute plus
        # height = 200
        dem_cover_ceiling = baseName + 'dem' + str(buffer2) + 'C'
        plus(dem_cover_base, int(height), dem_cover_ceiling)


        cellSize = arcpy.GetRasterProperties_management(dem_cover_base, "CELLSIZEY")

            
            

        #create skyline using skyline function
        skyline = skyline(dem_cover_base, point_6ft_name, bufferMeter1)
        #create two skyline barrier (multipatches) with skylineBarrier tool
        base_to_skyline = baseName + 'baseToSky'
        skylineBarrier(point_6ft_name, skyline, base_to_skyline, '0 METERS', '0 METERS')
        base_to_skylineExtend = baseName + 'base' + str(buffer3)
        skylineBarrier(point_6ft_name, skyline, base_to_skylineExtend, bufferMeter3, '0 METERS')
        #convert multipatch to raster with multipatch to raster tool
        base_to_skyline_ras = baseName + 'baseToSky_r'
        multipatchToRaster(base_to_skyline, base_to_skyline_ras)
        base_to_skylineExtend_ras = baseName + 'base' + str(buffer3) + '_r'
        multipatchToRaster(base_to_skylineExtend, base_to_skylineExtend_ras)

        #extract skyline raster by mask
        base_to_radius_ras = baseName + 'baseRad_r'
        clipRaster(base_to_skylineExtend_ras, bufferName_1, base_to_radius_ras)
        #clip 1000m dem to 800m
        dem_radius_base = baseName + 'dem' + str(radius_buffer) + 'B'
        clipRaster(dem_cover_base, bufferName_1, dem_radius_base)

        dem_radius_ceiling = baseName + 'dem' + str(radius_buffer) + 'C'
        clipRaster(dem_cover_ceiling, bufferName_1, dem_radius_ceiling)



        skyline_to_terrain = baseName + 'skyToTerr'
        cutFill(base_to_skyline_ras, dem_radius_base, skyline_to_terrain)
        ceiling_to_skyline = baseName + 'ceilToSky'
        cutFill(dem_radius_ceiling, base_to_radius_ras, ceiling_to_skyline)
        cylinder = baseName + 'cylinder'
        cutFill(dem_radius_ceiling, dem_radius_base, cylinder)


        #execute raster to polygon function
        skyline_to_terrain_pol = baseName + 'skyToTerr_pol'
        ceiling_to_skyline_pol = baseName + 'ceilToSky_pol'
        cylinder_pol = baseName + 'cylinder_pol'
        rasterToPolygon(skyline_to_terrain, skyline_to_terrain_pol)
        rasterToPolygon(ceiling_to_skyline, ceiling_to_skyline_pol)
        rasterToPolygon(cylinder, cylinder_pol)

        #add join
        skyline_to_terrain_join = arcpy.AddJoin_management(skyline_to_terrain_pol,'gridcode', skyline_to_terrain, 'VALUE')
        ceiling_to_skyline_join = arcpy.AddJoin_management(ceiling_to_skyline_pol,'gridcode', ceiling_to_skyline, 'VALUE')
        cylinder_join = arcpy.AddJoin_management(cylinder_pol, 'gridcode', cylinder, 'VALUE')

        #select by attribute for skyline to terrain polygon
        sql = 'VAT_' + skyline_to_terrain + '.VOLUME > 0'
        arcpy.SelectLayerByAttribute_management(skyline_to_terrain_join, 'NEW_SELECTION', sql)
        #make layer from selected features
        if arcpy.Exists('skyToTerr_pol_selection') and arcpy.env.overwriteOutput:  #'skyline_to_terrain_pol_selection'
                arcpy.Delete_management('skyToTerr_pol_selection')
        skyline_to_terrain_pol_selection = baseName + 'skyToTerr_pol_selection'
        arcpy.CopyFeatures_management(skyline_to_terrain_join, skyline_to_terrain_pol_selection)

        #spatial join
        #create a new fieldmappings and add the two input feature classes

        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable(bufferName_3)
        fieldmappings.addTable(skyline_to_terrain_pol_selection)
        fieldmapField = 'VAT_' + skyline_to_terrain + '_VOLUME'
        volume = fieldmappings.findFieldMapIndex(fieldmapField)
        fieldmap = fieldmappings.getFieldMap(volume)
        field = fieldmap.outputField
        field.name = 'VOLUME'
        fieldmap.outputField = field
        fieldmap.mergeRule = 'sum'
        fieldmappings.replaceFieldMap(volume,fieldmap)

        listField = arcpy.ListFields(skyline_to_terrain_pol_selection)
        # ls = []
        for f in listField:
            if not f.required:
                if f.name != fieldmapField:
                    x = fieldmappings.findFieldMapIndex(f.name)
                    fieldmappings.removeFieldMap(x)
                
        #spatial join for skyline to terrain
        skyToTerr_stat = baseName + 'skyToTerr_stat'
        if arcpy.Exists(skyToTerr_stat) and arcpy.env.overwriteOutput:
                arcpy.Delete_management(skyToTerr_stat)
        arcpy.SpatialJoin_analysis(bufferName_3, skyline_to_terrain_pol_selection, skyToTerr_stat, 'JOIN_ONE_TO_ONE','',fieldmappings)

        #spatial join for ceiling to skyline
        ceilToSky_stat = baseName + 'ceilToSky_stat'
        if arcpy.Exists(ceilToSky_stat) and arcpy.env.overwriteOutput:
                arcpy.Delete_management(ceilToSky_stat)
        arcpy.SpatialJoin_analysis(bufferName_3, ceiling_to_skyline_join, ceilToSky_stat)

        #spatial join for cylinder
        cylinder_stat = baseName + 'cylinder_stat'
        if arcpy.Exists(cylinder_stat) and arcpy.env.overwriteOutput:
            arcpy.Delete_management(cylinder_stat)
        arcpy.SpatialJoin_analysis(bufferName_3, cylinder_join, cylinder_stat)

        def deleteField(fc):
            lsField = arcpy.ListFields(fc)
            deleteLs = []
            for f in lsField:
                x = str(f.name)
                if not f.required:
                    if x != 'VOLUME':
                        if x.upper() != uID.upper():
                            deleteLs.append(f.name)
            return arcpy.DeleteField_management(fc, deleteLs)

        #delete unnecessary fields
        deleteField(skyToTerr_stat)
        deleteField(ceilToSky_stat)
        deleteField(cylinder_stat)

        #add field function
        def addField(newField, fc, fieldType):
            fields = arcpy.ListFields(fc, newField)
            if len(fields) != 1:
                arcpy.AddField_management(fc, newField, fieldType)
            else:
                pass
        
        #add four new fields to skyToTerr_stat
        visibleVolume = "visVolume"
        addField(visibleVolume, skyToTerr_stat, 'DOUBLE')
        notVisible = 'notVisible'
        addField(notVisible, skyToTerr_stat,'DOUBLE')
        total = 'totalVolume'
        addField(total, skyToTerr_stat, 'DOUBLE')
        visiblePercent = 'visPercent'
        addField(visiblePercent, skyToTerr_stat, 'DOUBLE')
        #join tables to obtain total visiblity
        visible = arcpy.AddJoin_management(skyToTerr_stat, uID, ceilToSky_stat, uID)
        # populate person_height field (THIS COULD BE A function)
        visible_sql = '!' + skyToTerr_stat + '.VOLUME! + ' + '!' + ceilToSky_stat + '.VOLUME!'
        arcpy.CalculateField_management(visible, skyToTerr_stat + '.' + visibleVolume, visible_sql, 'PYTHON3')
        #remove join
        # arcpy.RemoveJoin_management(skyToTerr_stat)

        #join table to obtain total volume of cylinder, percent of visibility and not visible volume
        total_join = arcpy.AddJoin_management(skyToTerr_stat, uID, cylinder_stat, uID)
        #not visible volume
        notVisible_sql = '!' + cylinder_stat + '.VOLUME! - ' + '!' + skyToTerr_stat + '.' + visibleVolume + '!'
        arcpy.CalculateField_management(total_join, skyToTerr_stat + '.' + notVisible, notVisible_sql, 'PYTHON3')
        
        #visible percent
        percentVis_sql = '(!' + skyToTerr_stat + '.' + visibleVolume + '! * 100) / !' + cylinder_stat + '.VOLUME!'
        arcpy.CalculateField_management(total_join, skyToTerr_stat + '.' + visiblePercent, percentVis_sql, 'PYTHON3')

        #total cylinder
        total_sql = '!' + cylinder_stat + '.VOLUME!'
        arcpy.CalculateField_management(total_join, skyToTerr_stat + '.' + total, total_sql, 'PYTHON3')
        arcpy.CopyRows_management(total_join, outTable)
        # arcpy.CopyFeatures_management(total_join, baseName + 'result')
        print("Complete")
    else:
        raise ShapeError('Input does not contain points')

except ShapeError as err:
    print(err[0])
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
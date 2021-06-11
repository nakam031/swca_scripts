import arcpy
import os
import time

start_time = time.time()

arcpy.env.overwriteOutput = True

def intersect(ds):
    arcpy.env.workspace = ds

    ls = arcpy.ListFeatureClasses()

    blmAll = r"N:\Projects\test.gdb\boundaries\BLMFieldOffice"
    cedar_city_sql = "admu_name = 'CEDAR CITY FIELD OFFICE'"
    caliente_sql = "admu_name = 'Caliente Field Office'"
    st_george_sql = "admu_name = 'ST GEORGE FIELD OFFICE'"
    fillmore_sql = "admu_name = 'FILLMORE FIELD OFFICE'"
    little_snake_sql = "admu_name = 'LITTLE SNAKE FIELD OFFICE'"
    rawlins_sql = "admu_name = 'Rawlins Field Office'"
    richfield_sql = "admu_name = 'RICHFIELD FIELD OFFICE'"
    salt_lake_sql = "admu_name = 'SALT LAKE FIELD OFFICE'"
    southern_nevada_sql = "admu_name = 'Southern Nevada Field Office'"
    vernal_sql = "admu_name = 'VERNAL FIELD OFFICE'"
    white_river_sql = "admu_name = 'WHITE RIVER FIELD OFFICE'"
    cedar_city = "cedar_city"
    arcpy.MakeFeatureLayer_management(blmAll,cedar_city,cedar_city_sql)
    caliente = "caliente"
    arcpy.MakeFeatureLayer_management(blmAll,caliente, caliente_sql)
    st_george = "st_george"
    arcpy.MakeFeatureLayer_management(blmAll,st_george, st_george_sql)
    fillmore = "fillmore"
    arcpy.MakeFeatureLayer_management(blmAll,fillmore,fillmore_sql)
    little_snake = "little_snake"
    arcpy.MakeFeatureLayer_management(blmAll,little_snake,little_snake_sql)
    rawlins = "rawlins"
    arcpy.MakeFeatureLayer_management(blmAll,rawlins,rawlins_sql)
    richfield = "richfield"
    arcpy.MakeFeatureLayer_management(blmAll,richfield,richfield_sql)
    salt_lake = "salt_lake"
    arcpy.MakeFeatureLayer_management(blmAll,salt_lake,salt_lake_sql)
    southern_nevada = "southern_nevada"
    arcpy.MakeFeatureLayer_management(blmAll,southern_nevada,southern_nevada_sql)
    vernal = "vernal"
    arcpy.MakeFeatureLayer_management(blmAll,vernal,vernal_sql)
    white_river = "white_river"
    arcpy.MakeFeatureLayer_management(blmAll,white_river,white_river_sql)
    blmLs = [cedar_city,caliente,st_george,fillmore,little_snake,rawlins, richfield,salt_lake,southern_nevada,vernal,white_river]

    for l in ls:
        flds = [f.name.lower() for f in arcpy.ListFields(l)]
        if "fieldoffice" in flds:
            pass
        else:
            print(l)
            
            appendLs = []
            arcpy.Delete_management("memory")
            for b in blmLs:
                outInt = f"memory/{b}Int"
                arcpy.Intersect_analysis([l,b],outInt,"ALL")
                if int(arcpy.GetCount_management(outInt)[0]) > 0:
                    appendLs.append(outInt)
                else:
                    pass
                    # print(f"nothing in {b} office")
            if len(appendLs) != 0:
                fieldMappings = arcpy.FieldMappings()
                fieldMappings.addTable(l)
                fieldMappings.addTable(b)
                # field_map = arcpy.FieldMap()
                # field_map.addInputField(l, "fieldoffice")
                # field_map.addInputField(outInt, "fieldoffice_1")
                # fieldMappings.addFieldMap(field_map)
                arcpy.DeleteRows_management(l)
                arcpy.AddField_management(l,"fieldoffice","TEXT","","",40)
                arcpy.Append_management(appendLs,l,"NO_TEST",fieldMappings,"")
            else:
                print("nothing was intersected")

if __name__ == '__main__':
    # ds = "N:\\Projects\\test.gdb\\planningCadastre"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\inlandWaterResource"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\sageGrouse"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\geoscientificInformation"
    # intersect(ds)
    
    # ds = "N:\\Projects\\test.gdb\\bigGame"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\visual"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\wildlife"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\society"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\sssWildlife"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\planningCadastre"
    # intersect(ds)
    # ds = "N:\\Projects\\test.gdb\\inlandWaterResource"
    # intersect(ds)
    ds = "N:\\Projects\\test.gdb\\sssPlants"
    intersect(ds)


    print("done")
    end_time = time.time()
    ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
    print('Completed in {} minutes.'.format(ttl_time))



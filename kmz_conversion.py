import arcpy, os, time

start_time = time.time()
arcpy.env.overwriteOutput = True

kmz = arcpy.GetParameterAsText(0)
# kmz = r"C:\Users\hitomi.nakamura\Documents\kmz_script\USACE_Tract.kmz"

direct = arcpy.GetParameterAsText(1)
arcpy.AddMessage("Convert KMZ to Layer: {}".format(direct))
arcpy.KMLToLayer_conversion(kmz,direct)
kmz_name = os.path.basename(kmz)[:-3]
database = '{}/{}gdb'.format(direct,kmz_name)
dataset = database + '/Placemarks'
arcpy.env.workspace = dataset
GCS_List = arcpy.ListFeatureClasses()

#coordinate system
sr = arcpy.GetParameterAsText(2)
# sr = arcpy.SpatialReference("NAD 1983 UTM Zone 14N")

i = 0

for fc in GCS_List:
    
    outfc = "{}\\{}_project".format(database, fc)
    arcpy.AddMessage("reproject feature class: {}".format(outfc))
    arcpy.Project_management(fc, outfc, sr)

arcpy.env.workspace = database
project_list = arcpy.ListFeatureClasses()


keep_fields = ['OID', 'Shape', 'SHAPE', 'PopupInfo', 'Shape_Length', 'Shape_Area', 'SHAPE_Length', 'SHAPE_Area', 'Name']
edit_field = ['PopupInfo']
arcpy.AddMessage("Update attribute table")
for fc in project_list:
    arcpy.AddMessage(fc)
    with arcpy.da.SearchCursor(fc, edit_field) as cursor:
        for row in cursor:
            pop_string = row[0]
            pop_array = pop_string.split("<")
            fields_array = []
            names_array = []

            for tag in pop_array:
                if "td>" in tag and "/td>" not in tag:
                    fields_array.append(tag)
            break
        
        for fields in arcpy.ListFields(fc):
            if fields.name not in keep_fields:
                arcpy.DeleteField_management(fc,fields.name)
        
        del fields_array[:2]

        for x in range(0, len(fields_array)):
            fields_array[x]=fields_array[x].replace("td>","")
            if x%2 == 0 and fields_array[x] not in keep_fields:
                names_array.append(fields_array[x])
                arcpy.AddField_management(fc, fields_array[x], "TEXT")
        

        names_array.append("PopupInfo")

        with arcpy.da.UpdateCursor(fc, names_array) as cursor:
            for row in cursor:

                pop_string = row[-1]
                pop_array = pop_string.split("<")
                fields_array = []
                values_array = []

                for segment in pop_array:
                    if "td>" in segment and "/td>" not in segment:
                        fields_array.append(segment)
                
                del fields_array[:2]

                for x in range(0,len(fields_array)):
                    if x%2 != 0:
                        if fields_array[x-1] not in keep_fields:
                            fields_array[x]=fields_array[x].replace("td>","")
                            values_array.append(fields_array[x])
                
                for y in range(0,len(values_array)):
                    try:
                        row[y] = values_array[y]
                        cursor.updateRow(row)
                    except IndexError:
                        i += 1


arcpy.AddMessage("--- {} minutes ---".format(str((time.time() - start_time)/60)))                       
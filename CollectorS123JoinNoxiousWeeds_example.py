import arcpy, time
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayerCollection, FeatureSet, FeatureLayer, GeoAccessor
gis = GIS(url="",username="",password="",profile="")#add url, username, password and profile for the portal

## Helper Functions
def get_time():
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")
    return now_str

def clean_field(fl,field_list):
    with arcpy.da.UpdateCursor(fl,field_list) as cursor:
        for row in cursor:
            row[0] = row[0].strip().lower()
            cursor.updateRow(row)
            
            
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r""#set workspace 
input_polygon = "https://webmap1.swca.com/server/rest/services/SLC15915_18/Noxious_Weeds/FeatureServer/0"
input_survey = "https://webmap1.swca.com/server/rest/services/Hosted/service_c10e5cabe7e94cfcb09f1155edf07a3b/FeatureServer/0"
target_layer = "https://webmap1.swca.com/server/rest/services/Hosted/Noxious_Weeds_with_Survey_Data/FeatureServer/0"
polygon = arcpy.MakeFeatureLayer_management(input_polygon,"noxiousWeedsPolygon")

with arcpy.da.SearchCursor(target_layer, ["site_id","smeqcreviewer","qcnotes"]) as cursor:
    for row in cursor:
        siteId = row[0].replace(" ","")
        sme = row[1]
        qcnote = row[2]
        expression = "Site_ID = '{}'".format(siteId)
        with arcpy.da.UpdateCursor(polygon, ["Site_ID","smeqcreviewer","qcnotes"], where_clause = expression) as upCursor:
            for upRow in upCursor:
                upRow[1] = sme
                upRow[2] = qcnote
                upCursor.updateRow(upRow)

temp_polygon = arcpy.CopyFeatures_management(input_polygon,"Noxious_Weeds_with_Survey_Data")
temp_survey = arcpy.CopyFeatures_management(input_survey,"NoxiousWeeds_survey")
## Use the clean_field function to trim and lower all the data.
clean_field(input_polygon,["Site_ID"])
clean_field(input_survey,["site_id"])

target_attribute = list(GeoAccessor.from_layer(FeatureLayer(target_layer)).columns)
polygon_attribute = list(GeoAccessor.from_layer(FeatureLayer(input_polygon)).columns)

target_attribute_list = (list(set(target_attribute) - set(polygon_attribute)))

arcpy.management.JoinField(temp_polygon, "Site_ID", temp_survey, "site_id", target_attribute_list)

arcpy.DeleteRows_management(target_layer)

fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(temp_polygon)
fieldmappings.mergeRule = 'First'
arcpy.Append_management(temp_polygon, target_layer,"NO_TEST", fieldmappings)

overwrite_item = Item(gis, 'f9729746e13d489eb3aab25107c04e2b')
overwrite_collection = FeatureLayerCollection.fromitem(overwrite_item)

item_prop = {'description': 'Updated on '+ get_time()}
overwrite_item.update(item_prop)
print("Overwrite Completed | " + get_time())
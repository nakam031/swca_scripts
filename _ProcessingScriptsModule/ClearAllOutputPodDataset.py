import arcpy
import os
import ClearDataset


if __name__ == '__main__':
    
    #delete output.gdb
    outputGdb = "N:\\Projects\\test.gdb"
    arcpy.env.workspace = outputGdb
    dsLs = arcpy.ListFeatureDatasets_management(feature_type = "Feature")
    ClearDataset.deleteFCs(outputGdb,dsLs)
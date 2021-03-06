import arcpy
import os


def deleteFCs(gdb, datasetLs):
    for ls in datasetLs:
        ds = os.path.join(gdb,ls)
        fcLs = arcpy.ListFeatureClasses_management(feature_dataset=ls)
        printLs = []
        for fc in fcLs:
            arcpy.Delete_management(fc)
            name = f"{ls}\\{fc}"
            printLs.append(name)
        print("Deleted fcs " + printLs)

def deleteRows(gdb,datasetLs):
    for ls in datasetLs:
        ds = os.path.join(gdb,ls)
        fcLs = arcpy.ListFeatureClasses_management(feature_dataset=ds)
        printLs = []
        for fc in fcLs:
            if int(arcpy.GetCount_management(fc)[0]) > 0:
                arcpy.DeleteRows_management(fc)
                name = f"{ls}\\{fc}"
                printLs.append(name)
        print("Rows Deleted " + printLs)

if __name__ == '__main__':
    pass
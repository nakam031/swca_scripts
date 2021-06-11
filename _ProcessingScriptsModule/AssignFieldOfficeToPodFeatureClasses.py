import AssignFieldOfficeToFeatureClasses
import arcpy
import os
import time

start_time = time.time()

arcpy.env.overwriteOutput = True

if __name__ == '__main__':
    ds = "N:\\Projects\\test.gdb\\planningCadastrePod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\inlandWaterResourcePod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\sageGrousePod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\geoscientificInformationPod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\bigGamePod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\visualPod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\wildlifePod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\societyPod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\soilPod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\sssPlantsPod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)
    ds = "N:\\Projects\\test.gdb\\sssWildlifePod"
    AssignFieldOfficeToFeatureClasses.intersect(ds)

    print("done")
    end_time = time.time()
    ttl_time = '{:.2f}'.format((end_time - start_time) / 60)
    print('Completed in {} minutes.'.format(ttl_time))


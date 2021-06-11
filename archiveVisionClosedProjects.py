import glob
import os
import pandas as pd
from math import floor
import zipfile
import shutil

def createMasterFolder(projectNumber,projectFolder):
    if not os.path.exists(r"C:\Users\hitomi.nakamura\Documents\temp\test\master"):
        os.makedirs(r"C:\Users\hitomi.nakamura\Documents\temp\test\master")
    os.makedirs(projectFolder)
    return projectFolder
def movetoMaster(srcList,destination):
    for src in srcList:
        shutil.move(src,destination)
def zipup(projectFolder):
    arcname = os.path.basename(projectFolder)
    root = os.path.dirname(projectFolder)
    shutil.make_archive(projectFolder,"zip",root,arcname)
    shutil.move(projectFolder+".zip",r"\\test\To_Offsite")
    shutil.rmtree(projectFolder)


#folder path
folder = r"C:\Users\hitomi.nakamura\Documents\temp\test"
#input - text file with project numbers
# archivingProjectsTable = input("text file with a list of project numbers to archive: ")
archivingProjectsTable = r"N:\VisionClosedProjects\VisionClosedProjects.txt"
df = pd.read_csv(archivingProjectsTable,sep=',',header=None)
df.columns = ["project_number"]

for i,r in df.iterrows():
    rowNumber = i
    projectNumber = r[0].split(".")[0]
    if projectNumber.isdigit():
        if len(projectNumber) == 5:
            directoryNumber = floor(int(projectNumber)/1000)*1000
            projectDirectory = os.path.join(folder,str(directoryNumber))
            keypath = f"{projectDirectory}/*{projectNumber}*"

        elif len(projectNumber) == 6:
            directoryNumber = floor(int(projectNumber)/10000)*10000
            projectDirectory = os.path.join(folder,str(directoryNumber))
            keypath = f"{projectDirectory}/*{projectNumber}*"
    else:
        keypath = f"{folder}/*/*{projectNumber}*"
    targetList = glob.glob(keypath)
    if len(targetList)>0:
        #change projectDirectory to the actual location
        projectFolder = os.path.join(r"C:\Users\hitomi.nakamura\Documents\temp\test\master", projectNumber)
        createMasterFolder(projectNumber,projectFolder)
        movetoMaster(targetList,projectFolder)
        # outname = f"{projectDirectory}/{projectNumber}"
        zipup(projectFolder)
        
        # zip(targetList,outname)
    # zipinDirectory = f"{projectDirectory}/*.zip"
    # zipLists = glob.glob(zipinDirectory)
    # destination = r"\\pco-gis-file01\To_Offsite"
    # if len(zipLists)>0:
    #     for z in zipLists:
    #         shutil.move(z,destination)
shutil.rmtree(r"C:\Users\hitomi.nakamura\Documents\temp\test\master")
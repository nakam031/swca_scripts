import arcpy
arcpy.env.workspace = r"N:\Projects\15000\15915_18_GatewayWestSegmentD1\gdb\stipulationScratch.gdb\raptor"

allRaptor = "N:\Projects\15000\15915_18_GatewayWestSegmentD1\gdb\GwwSegmentD1Master.gdb\biotaReport13N\RaptorNestCompile13N"
stream = "https://webmap1.swca.com/server/rest/services/SLC15915_18/Inland_Water_Reference/FeatureServer/0"
tempStream = arcpy.MakeFeatureLayer_management(stream, "tempStream")

# BLM_C_RPTR_01 = "memory/BLM_C_RPTR_01"
# BLM_C_RPTR_02_1 = "memory/BLM_C_RPTR_02_1"
# BLM_C_RPTR_02_2 = "memory/BLM_C_RPTR_02_2"
# BLM_C_RPTR_02_3 = "memory/BLM_C_RPTR_02_3"
# BLM_C_RPTR_03_1 = "memory/BLM_C_RPTR_03_1"
# BLM_C_RPTR_03_2 = "memory/BLM_C_RPTR_03_2"
# BLM_C_RPTR_04 = "memory/BLM_C_RPTR_04"
# BLM_C_RPTR_05 = "memory/BLM_C_RPTR_05"
# BLM_C_RPTR_06 = "memory/BLM_C_RPTR_06"
# BLM_C_RPTR_07 = "memory/BLM_C_RPTR_07"
# BLM_C_RPTR_08_1 = "memory/BLM_C_RPTR_08_1"
# BLM_C_RPTR_08_2 = "memory/BLM_C_RPTR_08_2"
# BLM_C_RPTR_09 = "memory/BLM_C_RPTR_09"
# BLM_C_RPTR_10 = "memory/BLM_C_RPTR_10"
# BLM_C_RPTR_11 = "memory/BLM_C_RPTR_11"
# BLM_R_RPTR_01_1 = "memory/BLM_R_RPTR_01_1"
# BLM_R_RPTR_01_2 = "memory/BLM_R_RPTR_01_2"
# BLM_R_RPTR_01_3 = "memory/BLM_R_RPTR_01_3"
# BLM_R_RPTR_01_4 = "memory/BLM_R_RPTR_01_4"
# BLM_R_RPTR_01_5 = "memory/BLM_R_RPTR_01_5"
# BLM_R_RPTR_01_6 = "memory/BLM_R_RPTR_01_6"
# BLM_R_RPTR_02_1 = "memory/BLM_R_RPTR_02_1"
# BLM_R_RPTR_02_2 = "memory/BLM_R_RPTR_02_2"
# BLM_R_RPTR_03_1 = "memory/BLM_R_RPTR_03_1"
# BLM_R_RPTR_03_2 = "memory/BLM_R_RPTR_03_2"
# BLM_R_RPTR_04_1 = "memory/BLM_R_RPTR_04_1"
# BLM_R_RPTR_04_2 = "memory/BLM_R_RPTR_04_2"
# BLM_R_RPTR_05_1 = "memory/BLM_R_RPTR_05_1"
# BLM_R_RPTR_05_2 = "memory/BLM_R_RPTR_05_2"
# BLM_R_RPTR_06_1 = "memory/BLM_R_RPTR_06_1"
# BLM_R_RPTR_06_2 = "memory/BLM_R_RPTR_06_2"
# BLM_R_RPTR_07_1 = "memory/BLM_R_RPTR_07_1"
# BLM_R_RPTR_07_2 = "memory/BLM_R_RPTR_07_2"
# BLM_R_RPTR_08_1 = "memory/BLM_R_RPTR_08_1"
# BLM_R_RPTR_08_2 = "memory/BLM_R_RPTR_08_2"
# BLM_R_RPTR_09_1 = "memory/BLM_R_RPTR_09_1"
# BLM_R_RPTR_09_2 = "memory/BLM_R_RPTR_09_2"
# BLM_R_RPTR_10_1 = "memory/BLM_R_RPTR_10_1"
# BLM_R_RPTR_10_2 = "memory/BLM_R_RPTR_10_2"
# BLM_R_RPTR_11_1 = "memory/BLM_R_RPTR_11_1"
# BLM_R_RPTR_11_2 = "memory/BLM_R_RPTR_11_2"
# BLM_R_RPTR_12_1 = "memory/BLM_R_RPTR_12_1"
# BLM_R_RPTR_12_2 = "memory/BLM_R_RPTR_12_2"
# BLM_R_RPTR_13_1 = "memory/BLM_R_RPTR_13_1"
# BLM_R_RPTR_13_2 = "memory/BLM_R_RPTR_13_2"

# BLM_C_RPTR_01SQL = "species = 'HL'"
# BLM_C_RPTR_02_1SQL = ""
# BLM_C_RPTR_02_2SQL = ""
# BLM_C_RPTR_02_3SQL = ""
# BLM_C_RPTR_03_1SQL = "species = 'FH' and status = 'ACTI'"
# BLM_C_RPTR_03_2SQL = "species = 'FH' and comments = 'Artificial Nest Platform'"#fix comment
# BLM_C_RPTR_04SQL = "species = 'GE' and comments = 'Artificial Nest Platform'"#fix comment
# BLM_C_RPTR_05SQL = ""
# BLM_C_RPTR_06SQL = ""
# BLM_C_RPTR_07SQL = ""
# BLM_C_RPTR_08_1SQL = ""
# BLM_C_RPTR_08_2SQL #all
# BLM_C_RPTR_09SQL = ""
# BLM_C_RPTR_10SQL = ""
# BLM_C_RPTR_11SQL = ""
# BLM_R_RPTR_01_1SQL = "species = 'HL' and status = 'ACTI'"
# BLM_R_RPTR_01_2SQL = ""#need to revisit
# BLM_R_RPTR_01_3SQL = "species = 'HL'"
# BLM_R_RPTR_01_4SQL = ""
# BLM_R_RPTR_01_5SQL = "species = 'HL' and status = 'ACTI'"
# BLM_R_RPTR_01_6SQL = ""
# BLM_R_RPTR_02_1SQL = ""
# BLM_R_RPTR_02_2SQL = ""
# BLM_R_RPTR_03_1SQL = "species = 'FH' and status = 'ACTI'"
# BLM_R_RPTR_03_2SQL = "species = 'FH' and status = 'ACTI'"
# BLM_R_RPTR_04_1SQL = ""
# BLM_R_RPTR_04_2SQL = ""
# BLM_R_RPTR_05_1SQL = "species = 'GE' and status = 'ACTI'"
# BLM_R_RPTR_05_2SQL = "species = 'GE' and status = 'ACTI'"
# BLM_R_RPTR_06_1SQL = ""
# BLM_R_RPTR_06_2SQL = ""
# BLM_R_RPTR_07_1SQL = ""
# BLM_R_RPTR_07_2SQL = ""
# BLM_R_RPTR_08_1SQL = ""
# BLM_R_RPTR_08_2SQL = ""
# BLM_R_RPTR_09_1SQL = ""
# BLM_R_RPTR_09_2SQL = ""
# BLM_R_RPTR_10_1SQL = "status = 'ACTI'"
# BLM_R_RPTR_10_2SQL = "status = 'ACTI'"
# BLM_R_RPTR_11_1SQL = ""
# BLM_R_RPTR_11_2SQL = ""
# BLM_R_RPTR_12_1SQL = ""
# BLM_R_RPTR_12_2SQL = ""
# BLM_R_RPTR_13_1SQL = ""
# BLM_R_RPTR_13_2SQL = ""

inList = [["memory/BLM_C_RPTR_01","species = 'HL'",'1 Miles'],
["memory/BLM_C_RPTR_03_1","species = 'FH' and status = 'ACTI'",'0.5 Miles'],["memory/BLM_R_RPTR_01_1","species = 'HL' and status = 'ACTI'",'1 Miles'],
["memory/BLM_R_RPTR_01_3","species = 'HL'",'2.5 Miles'],["memory/BLM_R_RPTR_03_1","species = 'FH' and status = 'ACTI'",'1 Miles'],
["memory/BLM_R_RPTR_03_2","species = 'FH' and status = 'ACTI'",'1200 Feet'],["memory/BLM_R_RPTR_05_1","species = 'GE' and status = 'ACTI'",'1 Miles'],
["memory/BLM_R_RPTR_05_2","species = 'GE' and status = 'ACTI'",'825 Feet'],["memory/BLM_R_RPTR_10_1","status = 'ACTI'",'0.75 Miles'],
["memory/BLM_R_RPTR_10_1","status = 'ACTI'",'825 Feet']]
outList = []
for i in inList:
    outFc = i[0]
    sql = i[1]
    distance = i[2]
    if outFc == "memory/BLM_R_RPTR_01_3":
        if arcpy.Exists("tempLayer"):
            arcpy.Delete_management("tempLayer")
        arcpy.MakeFeatureLayer_management(allRaptor,"tempLayer",sql)
        tempbuffer = "memory/BLM_R_RPTR_01_3_2"
        arcpy.Buffer_analysis("tempLayer", tempbuffer, distance)
        clipStream = "memory/clipStream"
        arcpy.Clip_analysis(tempStream, tempbuffer, clipStream)
        arcpy.Buffer_analysis(clipStream,outFc,'0.5 Miles')
        outList.append(outFc,tempbuffer)
    else:
        if arcpy.Exists("tempLayer"):
            arcpy.Delete_management("tempLayer")
        arcpy.MakeFeatureLayer_management(allRaptor,"tempLayer",sql)
        arcpy.Buffer_analysis("tempLayer", outFc, distance)

        outList.append(outFc)
arcpy.Merge_management(outList,"RaptorStipulation","","ADD_SOURCE_INFO")
import arcpy
import os
from numpy.lib import twodim_base
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from functools import reduce
import TWEUltimateTable


rawlins = TWEUltimateTable.DataFrame('Rawlins')
littleSnake = TWEUltimateTable.DataFrame('Little Snake')
whiteRiver = TWEUltimateTable.DataFrame('White River')
vernal = TWEUltimateTable.DataFrame('Vernal')
saltLake = TWEUltimateTable.DataFrame('Salt Lake')
richfield = TWEUltimateTable.DataFrame('Richfield')
fillmore = TWEUltimateTable.DataFrame('Fillmore')
cedarCity = TWEUltimateTable.DataFrame('Cedar City')
caliente = TWEUltimateTable.DataFrame('Caliente')
lasVegas = TWEUltimateTable.DataFrame('Las Vegas')

outputxlsx = r"N:\Projects\outtest.xlsx"
with pd.ExcelWriter(outputxlsx) as writer:
    rawlins.to_excel(writer,sheet_name = 'Rawlins FO',index=False)
    littleSnake.to_excel(writer,sheet_name= 'Little Snake FO', index=False)
    whiteRiver.to_excel(writer,sheet_name= 'White River FO', index=False)
    vernal.to_excel(writer,sheet_name= 'Vernal FO', index=False)
    saltLake.to_excel(writer,sheet_name= 'Salt Lake FO - USFS', index=False)
    richfield.to_excel(writer,sheet_name= 'Richfield FO', index=False)
    fillmore.to_excel(writer,sheet_name= 'Fillmore FO', index=False)
    cedarCity.to_excel(writer,sheet_name= 'Cedar City FO', index=False)
    caliente.to_excel(writer,sheet_name= 'Caliente FO', index=False)
    lasVegas.to_excel(writer,sheet_name= 'Las Vegas FO', index=False)
    
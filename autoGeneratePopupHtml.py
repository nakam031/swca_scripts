import pandas as pd
import time

start_time = time.time()



excel = r""#replace with xlsx
df = pd.read_excel(excel,None)
sheetNameList = list(df.keys())

for sheetName in sheetNameList:
    mainList = ["<table>","<tbody>"]
    df = pd.read_excel(excel, sheet_name = sheetName)
    ls = df.values.tolist()
    for l in ls:
        appending = '<tr><th style="text-align: left; padding-left: 8px; padding-top:4px; color: grey;"><b>{}</b></th><td style="text-align: left; padding-left: 8px; padding-top:4px;">{}</td></tr>'.format(l[0],l[1])
        mainList.append(appending)
        
    lastAppend = '</tbody></table>'
    mainList.append(lastAppend)
    listToStr = '\n'.join(map(str, mainList))
    htmlFileName = "htmlCodeForCustomPopup\\{}Popup.html".format(sheetName)###replace with actual path
    with open(htmlFileName, "w") as file1:
        file1.write(listToStr)

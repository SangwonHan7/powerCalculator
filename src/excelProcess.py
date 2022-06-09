import pandas as pd
import os

def createExcelFile(result):
    data = pd.DataFrame(result, columns=[ '전투력'])
    xlxs_dir='./data/report.xlsx'
    if not os.path.isdir('./data'):                                                          
        os.mkdir('./data')
    with pd.ExcelWriter(xlxs_dir) as writer:
        data.to_excel(writer, sheet_name = 'data')
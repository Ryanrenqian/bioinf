###################################################################
# File Name: excel_merge.py
# Author: renqian
# mail: renqian@yucebio.com
# Created Time: Fri 22 Sep 2017 09:12:49 AM CST
#=============================================================
#!/usr/bin/env python3
import sys
files=sys.argv[3:]
suffix=sys.argv[2]
output=sys.argv[1]
import pandas as pd
def write_to(ExcelWriter,sheet,file):
    if file.endswith('txt') or file.endswith('xls'):
        data=pd.read_table(file,header=0,index_col=0, low_memory=False)
    elif file.endswith('.csv'):
        data=pd.read_table(file,header=0,index_col=0, low_memory=False)
    return data.to_excel(ExcelWriter,sheet_name=sheet)
#    del data

ExcelWriter =pd.ExcelWriter(output)
for file in files:
    sheet=file.split('/')[-1].split('.')[0]
    print (file,sheet,output)
 #   if file.endswith('txt') or file.endswith('xls'):
  #      data=pd.read_table(file,header=0,index_col=0, low_memory=False)
  #  elif file.endswith('.csv'):
  #      data=pd.read_table(file,header=0,index_col=0, low_memory=False)
#    data.to_excel(ExcelWriter,sheet_name=sheet)
#    del data 
    write_to(ExcelWriter,sheet,file)
ExcelWriter.save()

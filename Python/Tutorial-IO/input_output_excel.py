#!/usr/bin/env python3
################################################################################
# Excel
#
# Sources
# - https://openpyxl.readthedocs.io/en/default/index.html
# - https://xlsxwriter.readthedocs.io
# - https://www.datacamp.com/community/tutorials/python-excel-tutorial
# - https://realpython.com/openpyxl-excel-spreadsheets-python/
################################################################################
print(f"\n===== Running {__file__} =====\n")
#import xlrd
#import xlwt # no longer maintained
#import xlsxwriter
#import openpyxl
#import pyexcel
import pandas as pd
#pd.ExcelFile

data = {
    "Jan" : list(range(0,10)),
    "Feb" : list(range(10,20)),
    "Mar" : list(range(20,30)),
    "Apr" : list(range(30,40)),
}
indexes = [
    'Income 1',
    'Income 2',
    'Income 3',
    'Fixed Cost 1',
    'Fixed Cost 2',
    'Fixed Cost 3',
    'Semi Variable Cost 1',
    'Semi Variable Cost 2',
    'Highly Variable Cost 1',
    'Highly Variable Cost 2',
]
df = pd.DataFrame(data, index=indexes)
df = df + 0.01
xls_opath = 'test_excel.xlsx'
sheet_name = '2022'
# Basic formatting
# df.to_excel(
#     excel_writer = xls_opath,
#     sheet_name = 'MySheet',
#     startrow = 2,
#     startcol = 1,
# )

# ExcelWriter
writer = pd.ExcelWriter(
            path = xls_opath,
            engine = 'xlsxwriter',
        )
# df.to_excel(
#     excel_writer = writer,
#     sheet_name = sheet_name,
#     startrow = 2,
#     startcol = 1,
#     verbose = True,
# )

# Formatting excel file
pd.DataFrame().to_excel(writer, sheet_name)
#df.iloc[0:0].to_excel(
#    excel_writer = writer,
#    sheet_name = sheet_name,
#    startrow = 2,
#    startcol = 1,
#)
#df.iloc[0:3].to_excel(writer, sheet_name, startrow=4, startcol=1, header=False)
#
#df.iloc[3:6].to_excel(writer, sheet_name, startrow=4+3+4, startcol=1, header=False)
#
#df.iloc[6:8].to_excel(writer, sheet_name, startrow=4+3+4+3+2, startcol=1, header=False)
#df.iloc[8:11].to_excel(writer, sheet_name, startrow=4+3+4+3+2+2+2, startcol=1, header=False)
workbook = writer.book
worksheet = writer.sheets[sheet_name]


# Adjust column width
first_col, last_col = 1,1
width = max(map(len, indexes))+2
worksheet.set_column(first_col, last_col, width) 

# Write formatted cell
row = 1
col = 1
txt = '2022'
fmt = workbook.add_format({
    'bold'       : True,
    'font_color' : 'white',
    'bg_color'   : '#2B8A53',
    'border'     : 1,
})
#worksheet.write(row, col, txt, fmt)

# Write merged cell
first_row, last_row = 1, 1
first_col, last_col = 1, 5 
worksheet.merge_range(first_row, first_col, last_row, last_col, txt, fmt)

txt = 'Income'
fmt = workbook.add_format({
    'bold'       : True,
    'bg_color'   : '#D0E7C9',
    'border'     : 1,
})
first_row, last_row = 3, 3
first_col, last_col = 1, 5 
worksheet.merge_range(first_row, first_col, last_row, last_col, txt, fmt)

txt = ''
fmt = workbook.add_format({
    'bg_color': 'white',
    'left'    : 1,
    'right'   : 1,
})
first_row, last_row = 8, 8
first_col, last_col = 1, 5 
worksheet.merge_range(first_row, first_col, last_row, last_col, txt, fmt)

txt = 'Expenses'
fmt = workbook.add_format({
    'bold'       : True,
    'bg_color'   : '#D0E7C9',
    'bottom'     : 1,
})
first_row, last_row = 9, 9
first_col, last_col = 1, 5 
worksheet.merge_range(first_row, first_col, last_row, last_col, txt, fmt)

row = 10
col = 1
txt = 'Fixed Costs'
fmt = workbook.add_format({
    'bold'  : True,
    'align' : 'center',
    'bg_color'   : 'white',
})
worksheet.write(row, col, txt, fmt)

# Add formulas
for col in range(2,6):
    row = 7
    col_let = 'ABCDEFG'[col]
    formula = f'=SUM({col_let}5:{col_let}7)'
    fmt = workbook.add_format({
        'align' : 'right',
        'bg_color'   : '#B5CF8A',
        'num_format' : 42, # currency
        'border'     : 1,
    })
    worksheet.write_formula(row, col, formula, fmt)

# Update formatting
for row in range(4,7):
    col = 1
    txt = df.index[row-4]
    fmt = workbook.add_format({
        'align'    : 'left',
        'bg_color' : 'white',
        'left'     : 1,
        'right'    : 1,
    })
    worksheet.write(row, col, txt, fmt)

# Add a comment
worksheet.write_comment('C5', 'Test Comment')
worksheet.write_comment('C6', 'Test comment 1.\n Test comment 2')
worksheet.write_comment('C7', 'X'*100)

writer.close()
print('File saved:', xls_opath)




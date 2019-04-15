# this py for get useful data for txn_statis

import xlrd,xlwt
import xlutils.copy
import re
import random


def getDataSet(sheetName,col_arg):
    nowSheet = excelFile.sheet_by_name(sheetName)
    dataList = []
    for col_i in col_arg:
        col_vals = nowSheet.col_values(col_i)
        dataList.append(col_vals)
    dataList.append(sheetName)
    return dataList

def converToInt(mylist):
    del mylist[0]
    return [int(x.strip()) for x in mylist]

def converCellToInt(cellVal):
    return int(cellVal.strip())

def convertCol(sheet_i,col_arg):
    nowSheet = excelFile.sheet_by_name(allsheet[sheet_i])
    wSheet = excelWrite.get_sheet(sheet_i) 
    rowCnt = nowSheet.nrows
    for col_i in col_arg:
        for row_i in range(rowCnt):
            if(row_i == 0):
                continue
            res = converCellToInt(nowSheet.cell_value(row_i,col_i))
            wSheet.write(row_i,col_i,res)
        print(allsheet[sheet_i] +"@"+nowSheet.cell_value(0,col_i)+ ":convert " + str(rowCnt) +"rows")


#main
excelFileName = 'runExcel.xlsx'
excelFile = xlrd.open_workbook(excelFileName);
excelWrite = xlutils.copy.copy(excelFile)
allsheet = excelFile.sheet_names()
sheetCnt = excelFile.nsheets

col_arg = {1}

for si in range(sheetCnt):
    convertCol(si,col_arg)

excelWrite.save(excelFileName)
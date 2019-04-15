import os, sys, re, os.path
import xlwt

excel_file = xlwt.Workbook()

COL_NAME = ['TXN_ID','CPU_TIME','START_TIME','TXN_RESULT','TXN_TYPE','READ_COUNT','WRITE_COUNT','SCAN_COUNT','GET_QUERY_TIME','INDEX_TIME','CC_TIME']

def initSheetHeader(sheetName , xlFile):
    xlSheet = xlFile.add_sheet(sheetName,True)
    colCnt = 0
    for col in COL_NAME:
        xlSheet.write(0,colCnt,col)
        colCnt = colCnt + 1
    return xlSheet

def saveIntoSheet(fileName,xlSheet):
    # open file -> get data for each txn ->write into excel sheet
    row_index = 1
    with open(fileName,'rt') as f:
        for line in f:
            chars = line.split(" ")
            if(chars[0] in COL_NAME):
                col_index = COL_NAME.index(chars[0])
                xlSheet.write(row_index,col_index,chars[2])
                if(col_index == len(COL_NAME)-1):
                    row_index = row_index+1
    print("save "+fileName+" success")


#main
inforDir = './runInfor'
inforFiles = [_file for _file in os.listdir(inforDir) if _file.endswith('.txt')]
workbook  = xlwt.Workbook()

for _file in inforFiles:
    sheet_name = _file.split('.')[0]
    nowSheet = initSheetHeader(sheet_name,workbook)
    print(sheet_name)
    saveIntoSheet("./runInfor/"+_file,nowSheet)

workbook.save('runExcel.xlsx')

print('Convert Success')   

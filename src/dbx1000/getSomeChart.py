import matplotlib.pyplot as plt 
import numpy as np 
import xlrd
import re


def getSheetName(sheet_arg):
    for sheetName in allsheet:
        found = True
        for k,v in sheet_arg.items():
            pa = k + str(v)
            if(re.search(pa,sheetName)==None):
                found = False
        if(found == True):
            break
    return sheetName

def getDataSet(sheetName,col_arg):
    nowSheet = excelFile.sheet_by_name(sheetName)
    dataList = []
    for col_i in col_arg:
        col_vals = nowSheet.col_values(col_i)
        #print(col_vals[0])
        #print(col_vals[1])
        dataList.append(col_vals)
    dataList.append(sheetName)
    return dataList

def converToInt(mylist):
    del mylist[0]
    return [int(x.strip()) for x in mylist]

def calAver(mylist):
    sum  = 0
    count = 0
    for item in mylist:
        sum = sum + item
        count = count + 1
    return sum / count

def showScatter(chartName,xname,x,yname,y):
    plt.figure()
    plt.title(chartName)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.scatter(x,y)
    plt.savefig('./runInfor/'+chartName+'-'+xname+'.png')
    #plt.show()

def showBar(chartName,xname,x,yname,y):
    plt.title(chartName)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.bar(x,y)
    plt.show()

##scatter show
def runScatterForEachTest():
    s_arg_list = [[6,2],[6,5],[6,8],[9,2]] 
    s_dict = {
        'theta' : 0,
        'WR' : 0
    }
    c_arg_list = [[6,1],[5,1]]
    
    for c_arg in c_arg_list:
        for s_arg in s_arg_list:
            s_dict['theta'] = s_arg[0]
            s_dict['WR'] = s_arg[1]
            sheetName = getSheetName(s_dict)
            dataList = getDataSet(sheetName,c_arg)
            showScatter(dataList[2],dataList[0][0],converToInt(dataList[0]),dataList[1][0],converToInt(dataList[1]))

##bar show
def runBarForAverageTime():
    s_arg_list = [[6,2],[6,5],[6,8],[9,2]] 
    s_dict = {
        'theta' : 0,
        'WR' : 0
    }
    c_arg = [1]

    aver_list = []
    name_list = []
    for s_arg in s_arg_list:
        s_dict['theta'] = s_arg[0]
        s_dict['WR'] = s_arg[1]
        sheetName = getSheetName(s_dict)
        dataList = getDataSet(sheetName,c_arg)
        intList = converToInt(dataList[0])
        aver_list.append(calAver(intList))
        name_list.append(sheetName)
    showBar("Average Time Compare","Condition",name_list,"Averge Time",aver_list)
    



#main
excelFileName = 'runExcel.xlsx'
excelFile = xlrd.open_workbook(excelFileName);
allsheet = excelFile.sheet_names()
#runScatterForEachTest()
runBarForAverageTime()
print(allsheet)
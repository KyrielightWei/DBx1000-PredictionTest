import matplotlib.pyplot as plt 
import numpy as np 
import xlrd
import re
import random


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
    #print(col_arg)
    for col_i in col_arg:
        col_vals = nowSheet.col_values(col_i)
        #print(len(col_vals))
        #print(col_vals[0])
        #print(col_vals[1])
        #print(col_i)
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
    #plt.figure()
    #print(xname)
    #print(yname)
    
    plt.title(chartName)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.scatter(x,y)
    plt.savefig('./runInfor/Scatter-'+chartName+'-'+xname+'.png')
    #plt.show()

def showBar(chartName,xname,x,yname,y):
    plt.title(chartName)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.bar(x,y)
    for valx,valy in zip(x,y):
        plt.text(valx, valy, int(valy), ha='center', va='bottom')
    #plt.savefig('./runInfor/Bar-'+chartName+'-'+xname+'.png')
    plt.show()


##scatter show 
def runScatterForEachTest():
    s_arg_list = [[6,2],[6,5],[6,8],[9,2]] 
    s_dict = {
        'theta' : 0,
        'WR' : 0
    }
    c_arg_list = [[6,1],[5,1]]
    
    #scatter
    for c_arg in c_arg_list:
        for s_arg in s_arg_list:
            s_dict['theta'] = s_arg[0]
            s_dict['WR'] = s_arg[1]
            sheetName = getSheetName(s_dict)
            dataList = getDataSet(sheetName,c_arg)
            name_list = []
            name_list.append(dataList[0][0])
            name_list.append(dataList[1][0])
            intList = []
            intList.append(converToInt(dataList[0]))
            intList.append(converToInt(dataList[1]))
            #show Scatter for each test
            #showScatter(dataList[2],name_list[0],intList[0],name_list[1],intList[1])
            #cal aver data 
            sum_dict = {}
            count_dict = {}
            for i in range(len(intList[0])):
                index = intList[0][i]
                val = intList[1][i]
                if index not in count_dict.keys():
                    sum_dict[index] = 0
                    count_dict[index] = 0
                sum_dict[index] = sum_dict[index] + val
                count_dict[index] = count_dict[index] + 1
            aver_index_list = range(17)
            aver_val_list = []
            for k in aver_index_list:
                if k not in sum_dict.keys():
                    aver_val_list.append(0)
                else:
                    aver_val_list.append(int(sum_dict[k]/count_dict[k]))
            #show aver bar 
            showBar(dataList[2] + "Aver Time",name_list[0],aver_index_list,name_list[1],aver_val_list)          

 
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
    
def showBarForDistribution(charTitle,barDict,rCnt,minV=0,maxV=0):
    # generate range
    max_val = 0
    min_val = 0
    for k,v in barDict.items():
        if(max_val == 0 and min_val == 0):
            max_val = max(v)
            min_val = min(v)
        if(max(v) > max_val):
            max_val = max(v)
        if(min(v) < min_val):
            min_val = min(v)
    if(minV != 0):
        min_val = minV
    if(maxV != 0):
        max_val = maxV
    step = int((max_val - min_val)/rCnt)
    bound_list  = []
    for i in range(rCnt):
        bound_list.append(min_val+(i)*step)
    bound_list.append(max_val)
    key_len  =  len(barDict)
    countList = []
    for i in range(key_len):
        countList.append([0]*rCnt)
    # start count
    key_i = 0;
    for k,v in barDict.items():
        for val in v:
            for i in range(rCnt):
                if(val >= bound_list[i] and val <= bound_list[i+1]):
                    break
            countList[key_i][i] = countList[key_i][i] + 1 
        key_i = key_i + 1
    # show bar
    bar_width = 0.2
    fig,ax = plt.subplots()
    index = np.arange(rCnt)
    key_i = 0
    #print(countList[key_i])

    for k in  barDict.keys():
        ax.bar(index+bar_width*key_i,countList[key_i],bar_width,color=(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)),label=k)
        for x,y in zip(index+bar_width*key_i,countList[key_i]):
            ax.text(x,y,int(y),ha='center', va='bottom')
        key_i = key_i + 1
    
    for i in range(key_len):
        print(countList[i])
    
    ax.set_xlabel('Distribution')
    ax.set_ylabel('Count')
    ax.set_title(charTitle)
    ax.set_xticks(index + bar_width* (key_len-1)/2 )
    rangeLsit = []
    for i in range(rCnt):
        rangeLsit.append(str(bound_list[i])+"-"+str(bound_list[i+1]))
    ax.set_xticklabels(rangeLsit)
    ax.legend()
    fig.tight_layout()
    plt.show()
    print("Distribution Bar has already generated")
    return bound_list;


def getListSlice(mylist,sliceCnt,index):
    mylist.sort()
    return mylist[index*sliceCnt:(index+1)*sliceCnt]

def runDisBarForAllTest():
    s_arg_list = [[6,2],[6,5],[6,8],[9,2]] 
    s_dict = {
        'theta' : 0,
        'WR' : 0
    }
    c_arg = [1]
    
    dict = {}
    slice_dict = {}
    for s_arg in s_arg_list:
        s_dict['theta'] = s_arg[0]
        s_dict['WR'] = s_arg[1]
        sheetName = getSheetName(s_dict)
        dataList = getDataSet(sheetName,c_arg)
        intList = converToInt(dataList[0])
       # print(len(dataList[0]))
       # print(len(intList))
        dict[sheetName] = intList
    
    max1,intver1 = showPlotForDistribution("All Test Time Distribution",dict,1000000)
    '''
    max1_1,intver1_1 = showPlotForDistribution("First Part Time Distribution",dict,maxV=intver1,interval=intver1/10)
    max1_1_1,intver1_1_1 = showPlotForDistribution("1.1 Part Time Distribution",dict,maxV=intver1_1,interval=intver1_1/10)
    max1_1_1_1,intver1_1_1_1 = showPlotForDistribution("1.1.1 Part Time Distribution",dict,maxV=intver1_1_1,interval=intver1_1_1/10)

    showPlotForDistribution("hlight Part Time Distribution",dict,maxV=16000,minV=4000,interval=1000)
    '''
    showPlotForDistribution("hlight Part2 Time Distribution",dict,maxV=13000,minV=6000,interval=500)
    #showPlotForDistribution("hlight Part2 Time Distribution",dict,maxV=23000,minV=8000,interval=1000)
    showPlotForDistribution("hlight Part2 Time Distribution",dict,maxV=10500,minV=9500,interval=50)
    '''
    b_list  = showBarForDistribution("All Test Time Distribution",dict,5)
    
    #print(b_list[0])
    #print(b_list[1])
    b_list1 = showBarForDistribution("First Part Time Distribution",dict,5,b_list[0],b_list[1])
    b_list1_1 = showBarForDistribution("1.1 Time Distribution",dict,5,b_list1[0],b_list1[1])
    b_list1_1_1 = showBarForDistribution("1.1.1 Time Distribution",dict,5,b_list1_1[0],b_list1_1[1])
    b_list1_1_1_1 = showBarForDistribution("1.1.1.1 Time Distribution",dict,5,b_list1_1_1[0],b_list1_1_1[1])
    b_list1_1_1_2 = showBarForDistribution("1.1.1.2 Time Distribution",dict,5,b_list1_1_1[1],b_list1_1_1[2])
    '''
    #for k,v in dict.items():
      #  slice_dict[k] = getListSlice(dict[k],int(len(dict[k])/5),0)
    #print(int(len(dict[k])))
    #showBarForDistribution("First Part Time Distribution",slice_dict,5)
    #print("all test")

colorStr = ['b','g','r','c','m','y','k']

def showPlotForDistribution(charTitle,plotDict,interval=1000,minV=0,maxV=0):
    # generate range
    max_val = 0
    min_val = 0
    for k,v in plotDict.items():
        if(max_val == 0 and min_val == 0):
            max_val = max(v)
            min_val = min(v)
        if(max(v) > max_val):
            max_val = max(v)
        if(min(v) < min_val):
            min_val = min(v)
    '''
    if(minV != 0):
        min_val = minV
    '''
    min_val = minV
    if(maxV != 0):
        max_val = maxV
    rangeVal  = max_val - min_val
    # generate count list
    interval = int(interval)
    rCnt = int(rangeVal / interval)
    if(rangeVal % interval != 0):
         rCnt = rCnt + 1
   # print(max_val)
    #print(rCnt)
    x_list = []
    for i in range(rCnt):
        x_list.append("["+str(int(min_val + i*interval))+","+str(int(min_val + (i+1)*interval))+")")
    count_list = [] 
    for k in plotDict.keys():
        count_list.append([0]*rCnt)
    #cal count
    key_i = 0
    cnt = 0
    for k,v in plotDict.items():
        for val in v:
            if(val <= max_val and val >= min_val):
                #print(val-min_val)
                if(val == max_val and (val-min_val) % interval == 0):
                    val = val - 1 
                #print(val)
                cnt = cnt + 1
                count_list[key_i][int((val-min_val)/ interval)] = count_list[key_i][int((val-min_val)/ interval)] + 1
        key_i = key_i + 1
    #show plot
    #x_list = [1,2,3]
    #count_list[0] = [100,180,64] 
    key_i = 0
    for k in plotDict.keys():
        #print(len(count_list[key_i]))
        plt.plot(x_list,count_list[key_i],colorStr[key_i]+'o--',label = k)
        key_i = key_i + 1
    plt.title(charTitle)
    plt.xlabel("Range")
    plt.ylabel("Count")
    plt.legend()
    plt.show()
    print(cnt)
    return max_val,interval

#main
excelFileName = 'runExcel.xlsx'
excelFile = xlrd.open_workbook(excelFileName);
allsheet = excelFile.sheet_names()
#runScatterForEachTest()
#runBarForAverageTime()
runDisBarForAllTest()
print(allsheet)
from functions import dataPreprocess
from functions import getTimeDifference
import numpy as np
import datetime
import time
#预处理数据
def preprocess(fileData,start_time,end_time,hour):
    # 数据清洗、基础的预处理
    # 这里开始考虑选取那些feature
    # 选取Time，Temperature，Pressure，Humidity作为输入信息，删除其他的列
    rawData = fileData[['TimeStamp','Temperature','Pressure','Humidity']]
    #pattern = '^(\d+)/(\d+)/(\d+)([\D]+)(\d+):(\d+):(\d+)$'
    myData = [] # 用于存放处理好数据的list
    for index, row in rawData.iterrows():
        rowTemp = []
        """
            # 处理Time
            timeStr = re.sub(pattern,lambda m: m.group(1)+'/'+m.group(2)+'/'+m.group(3)+' '+m.group(5)+':'+m.group(6)+':'+m.group(7),row['Time'])
            timeArray = time.mktime(time.strptime(timeStr,'%Y/%m/%d %H:%M:%S'))
            rowTemp.append(timeArray)
        """
        # 处理Time，时间戳拆分成多个部分
        # TODO:把生成时间戳的代码加入到里面
        rowTemp.append(row['TimeStamp'])
        dateTime = datetime.datetime.fromtimestamp(row['TimeStamp'])
        rowTemp.append(dateTime.month)
        rowTemp.append(dateTime.day)
        rowTemp.append(dateTime.hour)
        rowTemp.append(dateTime.minute)
        # 直接将剩下三列加到数组中
        rowTemp.append(row['Temperature'])
        rowTemp.append(row['Pressure'])
        rowTemp.append(row['Humidity'])
        # TODO:找到外部传感器的数据，把它加入到数据集中
        #      可能遇到的问题：时间如何对齐？
        myData.append(rowTemp)
    myData = myData[::-1]
    myData = np.array(myData)
    np.save("myData",myData)
    # 目前的数据格式 - 第一列：时间戳；第二列：月份；第三列：日期；第四列：小时；第五列：分钟；第六列：温度；第七列：压强；第八列：湿度

    data = np.load("myData.npy").astype(float)
    startTime = time.mktime(time.strptime(start_time,'%Y/%m/%d %H:%M:%S'))#开始时间
    endTime = time.mktime(time.strptime(end_time,'%Y/%m/%d %H:%M:%S'))#结束时间
    startMask = np.array(data[:,0] >= startTime, dtype='bool')
    endMask = np.array(data[:,0] <= endTime, dtype='bool')
    myData = data[startMask & endMask,:]
    data1 = dataPreprocess(myData, 15, hour*60)
    np.save("dataSet.npy", data1)
    #save = pd.DataFrame(data1)
    #save.to_csv('.\\abc.csv',index=False,header=False)  
def create_file(file_path,msg):
    f=open(file_path,"w")
    f.write(msg)
    f.close()

def getTimeDifference(timeStamp1, timeStamp2):
    # 判断两时间戳
    if timeStamp1 < timeStamp2:
        t = timeStamp1
        timeStamp1 = timeStamp2
        timeStamp2 = t
    seconds = timeStamp1 - timeStamp2
    return round(seconds/60)

"""
@FunctionName:
    dataPreprocess
@Input:
    rawData：list，要处理的数据
    inputDataScale：int，用于预测的数据行数
    predictDataRange：int，想要预测的时间（比如，取值为1时即预测1分钟后的溶解氧含量）
@Process:
    根据对原始数据滑窗处理，将inputDataScale行数据合并成一行数据作为预测的input，将predictDataRange行后传感器测得的溶解氧含量作为label，得到不同的dataSet
@Output:
    data：numpy，处理好的数据
"""
def dataPreprocess(rawData, inputDataScale, predictDataRange):
    predictTime = predictDataRange # 60
    data = []
    index = 0
    rowQueue = [] # 申请队列来存放新数据
    lastTimeStamp = rawData[0, 0]
    yIndex = 0
    # 当不能生成新的一行数据时，停止循环
    while index + predictDataRange < len(rawData):
        op = 1 # 执行操作的指示
        try:
            thisRow = rawData[index]
            timeStamp = thisRow[0]
        except:
            op = 2  # 当处理出错时，滑窗跳过这里
        queueLen = len(rowQueue)
        # 当队列为空时，将直接将本行处理好后加入队列
        if queueLen == 0:
            op = 1
        elif queueLen < inputDataScale - 1:
            if getTimeDifference(lastTimeStamp, timeStamp) == 1:
                op = 1
            else:
                op = 2
        else:
            op = 3
        # 根据op进行相应操作
        if op == 1:   
            # op=1:向队列加入新的一行
            lastTimeStamp = timeStamp
            rowQueue.append(thisRow)
            index = index + 1
        elif op == 2:
            # op=2:清空现有队列，从本行开始重新滑窗
            rowQueue = []
            lastTimeStamp = timeStamp
            rowQueue.append(thisRow)
            index = index + 1
        else:
            # op=3:队列已满，把该队列存到data里
            lastTimeStamp = timeStamp
            rowQueue.append(thisRow)
            index = index + 1
            if rawData[yIndex, 0] < rawData[index, 0]:
                    yIndex = index + 1
            while True:                
                yTimeStamp = rawData[yIndex, 0]
                if getTimeDifference(yTimeStamp, timeStamp) < predictTime:
                    yIndex = yIndex + 1
                    continue
                elif getTimeDifference(yTimeStamp, timeStamp) > predictTime:
                    rowQueue = []
                    rowQueue.append(thisRow)
                    break
                else:
                    newRow = []
                    newRow.append(float(rawData[yIndex, 5]))
                    for i in range(len(rowQueue)):
                        for j in range(len(rowQueue[0])):
                            if i == 0 or j > 4: # 剔除除了第一行之外的时间信息
                                newRow.append(float(rowQueue[i][j]))                    
                    rowQueue.pop(0)
                    data.append(newRow)     
                    break
    return data
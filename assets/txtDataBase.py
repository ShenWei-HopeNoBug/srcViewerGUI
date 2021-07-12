# -*- coding: GB2312 -*-

import os
import re

'''
返回状态:
    失败{
        'state':False,
        'reason':''
    }
    成功消息{
        'state':True,
        'msg':''
    }
    成功数据{
        'state':True,
        'data':''
    }
'''


# try捕获异常装饰器(txtDataBase专用)
def tryFunc(func):
    def decorator(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as err:
            return {
                'state': False,
                'reason': str(err)
            }

    return decorator


class TxtDatabase(object):
    def __init__(self, path):
        self.path = path
        self.encoding = 'GB2312'
        self.sumSignChar = '#'
        self.sumString = 'Sum'
        self.sumMaxBit = 64

    # -----------------------------基本方法
    # 检查路径
    @tryFunc
    def pathCheck(self):
        return os.path.exists(self.path)

    # 清除数据
    @tryFunc
    def clearAll(self):
        with open(self.path, 'w', encoding=self.encoding) as fl:
            fl.write('{}{}=0{}\n'.format(
                self.sumSignChar,
                self.sumString,
                self.sumSignChar * (self.sumMaxBit + 1)
            ))
        return {
            'state': True,
            'msg': '数据已全部清除{}=0'.format(self.sumString)
        }

    # 输出所有数据
    @tryFunc
    def printDatas(self):
        with open(self.path, 'r', encoding=self.encoding) as fl:
            data = fl.readlines()
        return {
            'state': True,
            'data': [data[1:].rstrip('\n') for index, data in enumerate(data) if index > 0]
        }

    # -----------------------------数据统计
    # 检查数据总数并格式化文件
    @tryFunc
    def sumCheck(self):
        count = 0
        with open(self.path, 'r', encoding=self.encoding) as fl:
            firstLine = fl.readline()
            fl.seek(0)
            while (fl.readline()):
                count += 1

        # 空文件
        if (count == 0):
            self.clearAll()
        # 已格式化db，修正数据总量
        elif (re.search(r'{}='.format(self.sumString), firstLine)):
            self.setDataSum(count - 1)
            count -= 1
        # 没格式化db
        else:
            bit = len(str(count))
            with open(self.path, 'r', encoding=self.encoding) as oldFile:
                with open(self.path, 'r+', encoding=self.encoding) as newFile:
                    # 写入第一行统计信息
                    newFile.write('{}{}={}{}\n'.format(
                        self.sumSignChar,
                        self.sumString,
                        count,
                        self.sumSignChar * (self.sumMaxBit + 2 - bit)
                    ))
                    # 写入原数据
                    line = oldFile.readline()
                    while (line):
                        newFile.write(self.sumSignChar + line)
                        line = oldFile.readline()
                    newFile.truncate()

        return {
            'state': True,
            'msg': '数据库文件已格式化修正{}={}'.format(self.sumString, count)
        }

    # 获取数据总数
    @tryFunc
    def getDataSum(self):
        with open(self.path, 'r', encoding=self.encoding) as fl:
            return {
                'state': True,
                'data': int(re.findall(r'(?<==)\d+', fl.readline())[0])
            }

    # 设置数据总数
    @tryFunc
    def setDataSum(self, dataSum):
        bit = len(str(dataSum))
        with open(self.path, 'r+', encoding=self.encoding) as fl:
            fl.write('{}{}={}{}'.format(
                self.sumSignChar,
                self.sumString,
                dataSum,
                self.sumSignChar * (self.sumMaxBit + 2 - bit)
            ))
        return {
            'state': True,
            'msg': '数据总数设置完成{}={}'.format(self.sumString, dataSum)
        }

    # -----------------------------增
    # 追加一条数据
    @tryFunc
    def addOneData(self, data, updata=True):
        with open(self.path, 'a+', encoding=self.encoding) as fl:
            fl.write('{}{}\n'.format(self.sumSignChar, data))
        if (updata):
            self.setDataSum(self.getDataSum()['data'] + 1)
        return {
            'state': True,
            'msg': data
        }

    # 添加多条数据
    @tryFunc
    def addDatas(self, dataArray):
        for index, data in enumerate(dataArray):
            self.addOneData(data, False)
        self.setDataSum(self.getDataSum()['data'] + len(dataArray))
        return {
            'state': True,
            'msg': dataArray
        }

    # -----------------------------查
    # 查找指定索引的数据内容(索引从1开始)
    # 超出范围的索引结果返回None
    # 返回一一对应的index序列
    @tryFunc
    def findIndexData(self, indexArray):
        indexLen = len(indexArray)
        dataSum = self.getDataSum()['data']
        # 统计范围内的数据量
        inCount = 0
        for index in indexArray:
            if (index > 0 and index <= dataSum):
                inCount += 1
        # -----输入为空或范围内数据量为0
        if (not indexLen or (not inCount)):
            return {
                'state': False,
                'reason': '输入查找索引序列为空或索引全部超出范围'
            }
        # -----开始查找指定索引数据
        maxIndex = max(indexArray)  # 输入序列最大索引
        if (maxIndex > dataSum):
            maxIndex = dataSum
        dataArray = [None] * indexLen  # 查找结果
        with open(self.path, 'r', encoding=self.encoding) as fl:
            fl.readline()
            curLine = 1
            while (curLine <= maxIndex + 1):
                # 保存查找结果
                if (curLine in indexArray):
                    dataArray[indexArray.index(curLine)] = fl.readline()[1:].rstrip('\n')
                    inCount -= 1
                else:
                    fl.readline()
                if (not inCount):
                    break
                curLine += 1

        return {
            'state': True,
            'data': dataArray
        }

    # 查找指定内容的数据索引(索引从1开始，不存在返回-1)
    # 返回{data1:[],data2:[]}
    @tryFunc
    def findDatas(self, dataArray):
        dataLen = len(dataArray)
        # ----输入为空
        if (not dataLen):
            return {
                'state': False,
                'reason': '输入查找内容序列为空'
            }
        dataSum = self.getDataSum()['data']
        indexDict = {data: [-1] for data in dataArray}  # 结果字典
        with open(self.path, 'r', encoding=self.encoding) as fl:
            fl.readline()
            for index in range(dataSum):
                data = fl.readline()[1:].rstrip('\n')
                if (data in dataArray):
                    if (indexDict[data][0] == -1):
                        indexDict[data][0] = index + 1
                    else:
                        indexDict[data].append(index + 1)

        return {
            'state': True,
            'data': indexDict
        }

    # 查找指定内容的一条数据的索引(索引从1开始，不存在返回-1)
    # 返回索引系列
    @tryFunc
    def findOneData(self, data):
        return {
            'state': True,
            'data': self.findDatas([data])['data'][data]
        }

    # ------------------------------改
    # 修改指定索引的数据(索引从1开始)
    # dataDict = {index1:'new1',index2:'new2'}
    @tryFunc
    def modifyIndexData(self, dataDict):
        # 滤除超出范围的索引
        dataSum = self.getDataSum()['data']
        dataDict = {key: value for key, value in dataDict.items()
                    if key > 0 and key <= dataSum}
        minIndex = min([index for index in dataDict.keys()])
        # 开始修改
        modifyDict = {}  # 修改细节
        with open(self.path, 'r', encoding=self.encoding) as oldFile:
            with open(self.path, 'r+', encoding=self.encoding) as newFile:
                curLine = 0
                # oldFile定位到修改行行首
                while (curLine < minIndex):
                    oldFile.readline()
                    curLine += 1
                # newFile同步定位
                newFile.seek(oldFile.tell() - 1)
                # 对指定索引内容进行修改
                nextLine = oldFile.readline()
                curLine += 1
                while (nextLine):
                    if ((curLine - 1) not in dataDict.keys()):
                        newFile.write(nextLine)
                    else:
                        newFile.write('{}{}\n'.format(self.sumSignChar, dataDict[curLine - 1]))
                        modifyDict[curLine - 1] = '{}=>{}'.format(
                            nextLine[1:].rstrip('\n'),
                            dataDict[curLine - 1]
                        )
                    nextLine = oldFile.readline()
                    curLine += 1
                newFile.truncate()
        return {
            'state': True,
            'msg': modifyDict
        }

    # 修改指定内容的数据
    # dataDict = {'old':'new1','old2':'new2'}
    @tryFunc
    def modifyDatas(self, dataDict):
        modifyDict = {}
        # 开始修改
        with open(self.path, 'r', encoding=self.encoding) as oldFile:
            with open(self.path, 'r+', encoding=self.encoding) as newFile:
                oldFile.readline()
                curLine = 1
                # newFile定位到第一条数据行首
                newFile.seek(oldFile.tell() - 1, 0)
                # 修改所有指定数据的内容
                nextLine = oldFile.readline()
                curLine += 1
                while (nextLine):
                    data = nextLine[1:].rstrip('\n')
                    if (data not in dataDict.keys()):
                        newFile.write(nextLine)
                    else:
                        newFile.write('{}{}\n'.format(self.sumSignChar, dataDict[data]))
                        modifyDict[curLine - 1] = '{}=>{}'.format(
                            data,
                            dataDict[data]
                        )
                    nextLine = oldFile.readline()
                    curLine += 1
                newFile.truncate()
        return {
            'state': True,
            'msg': modifyDict
        }

    # ------------------------------删
    # 删除指定索引的数据(索引从1开始)
    # 返回{index1:data1,index2:data2}
    @tryFunc
    def deleteIndexData(self, indexArray):
        # 输入为空
        if (not len(indexArray)):
            return {
                'state': False,
                'reason': '输入删除索引序列为空'
            }
        # 滤除超出范围的索引并升序排序
        dataSum = self.getDataSum()['data']
        indexArray = [index for index in indexArray if index > 0 and index <= dataSum]
        indexArray.sort()
        # 开始删除
        deleteDict = {}
        with open(self.path, 'r', encoding=self.encoding) as oldFile:
            with open(self.path, 'r+', encoding=self.encoding) as newFile:
                curLine = 0
                # oldFile定位到删除行的前一行
                while (curLine < indexArray[0]):
                    oldFile.readline()
                    curLine += 1
                # newFile同步定位
                newFile.seek(oldFile.tell() - 1, 0)
                # 将删除行以外的数据写入
                nextLine = oldFile.readline()
                curLine += 1
                while (nextLine):
                    if ((curLine - 1) not in indexArray):
                        newFile.write(nextLine)
                    else:
                        deleteDict[curLine - 1] = nextLine[1:].rstrip('\n')
                    nextLine = oldFile.readline()
                    curLine += 1
                newFile.truncate()

        self.setDataSum(self.getDataSum()['data'] - len(indexArray))
        return {
            'state': True,
            'msg': deleteDict
        }

    # 删除一个指定内容的所有数据
    # 返回删除索引序列
    @tryFunc
    def deleteOneData(self, data):
        index = self.findOneData(data)['data']
        self.deleteIndexData(index)

        return {
            'state': True,
            'msg': index
        }

    # 删除指定内容的所有数据
    # 返回{data1:[index1],data2:[index2]}
    @tryFunc
    def deleteDatas(self, dataArray):
        # 输入为空
        if (not len(dataArray)):
            return {
                'state': False,
                'reason': '输入删除内容序列为空'
            }
        # 开始删除
        count = 0
        deleteDict = {}  # 删除细节
        with open(self.path, 'r', encoding=self.encoding) as oldFile:
            with open(self.path, 'r+', encoding=self.encoding) as newFile:
                oldFile.readline()
                newFile.seek(oldFile.tell() - 1, 0)
                curLine = 1
                nextLine = oldFile.readline()
                curLine += 1
                # 将删除内容以外的数据写入
                while (nextLine):
                    data = nextLine[1:].rstrip('\n')
                    if (data not in dataArray):
                        newFile.write(nextLine)
                    else:
                        # 保存删除细节
                        if (data in deleteDict.keys()):
                            deleteDict[data].append(curLine - 1)
                        else:
                            deleteDict[data] = [curLine - 1]
                        count += 1
                    nextLine = oldFile.readline()
                    curLine += 1
                newFile.truncate()
        self.setDataSum(self.getDataSum()['data'] - count)

        return {
            'state': True,
            'msg': deleteDict
        }

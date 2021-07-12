# -*- coding: GB2312 -*-

import os
import re

'''
����״̬:
    ʧ��{
        'state':False,
        'reason':''
    }
    �ɹ���Ϣ{
        'state':True,
        'msg':''
    }
    �ɹ�����{
        'state':True,
        'data':''
    }
'''


# try�����쳣װ����(txtDataBaseר��)
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

    # -----------------------------��������
    # ���·��
    @tryFunc
    def pathCheck(self):
        return os.path.exists(self.path)

    # �������
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
            'msg': '������ȫ�����{}=0'.format(self.sumString)
        }

    # �����������
    @tryFunc
    def printDatas(self):
        with open(self.path, 'r', encoding=self.encoding) as fl:
            data = fl.readlines()
        return {
            'state': True,
            'data': [data[1:].rstrip('\n') for index, data in enumerate(data) if index > 0]
        }

    # -----------------------------����ͳ��
    # ���������������ʽ���ļ�
    @tryFunc
    def sumCheck(self):
        count = 0
        with open(self.path, 'r', encoding=self.encoding) as fl:
            firstLine = fl.readline()
            fl.seek(0)
            while (fl.readline()):
                count += 1

        # ���ļ�
        if (count == 0):
            self.clearAll()
        # �Ѹ�ʽ��db��������������
        elif (re.search(r'{}='.format(self.sumString), firstLine)):
            self.setDataSum(count - 1)
            count -= 1
        # û��ʽ��db
        else:
            bit = len(str(count))
            with open(self.path, 'r', encoding=self.encoding) as oldFile:
                with open(self.path, 'r+', encoding=self.encoding) as newFile:
                    # д���һ��ͳ����Ϣ
                    newFile.write('{}{}={}{}\n'.format(
                        self.sumSignChar,
                        self.sumString,
                        count,
                        self.sumSignChar * (self.sumMaxBit + 2 - bit)
                    ))
                    # д��ԭ����
                    line = oldFile.readline()
                    while (line):
                        newFile.write(self.sumSignChar + line)
                        line = oldFile.readline()
                    newFile.truncate()

        return {
            'state': True,
            'msg': '���ݿ��ļ��Ѹ�ʽ������{}={}'.format(self.sumString, count)
        }

    # ��ȡ��������
    @tryFunc
    def getDataSum(self):
        with open(self.path, 'r', encoding=self.encoding) as fl:
            return {
                'state': True,
                'data': int(re.findall(r'(?<==)\d+', fl.readline())[0])
            }

    # ������������
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
            'msg': '���������������{}={}'.format(self.sumString, dataSum)
        }

    # -----------------------------��
    # ׷��һ������
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

    # ��Ӷ�������
    @tryFunc
    def addDatas(self, dataArray):
        for index, data in enumerate(dataArray):
            self.addOneData(data, False)
        self.setDataSum(self.getDataSum()['data'] + len(dataArray))
        return {
            'state': True,
            'msg': dataArray
        }

    # -----------------------------��
    # ����ָ����������������(������1��ʼ)
    # ������Χ�������������None
    # ����һһ��Ӧ��index����
    @tryFunc
    def findIndexData(self, indexArray):
        indexLen = len(indexArray)
        dataSum = self.getDataSum()['data']
        # ͳ�Ʒ�Χ�ڵ�������
        inCount = 0
        for index in indexArray:
            if (index > 0 and index <= dataSum):
                inCount += 1
        # -----����Ϊ�ջ�Χ��������Ϊ0
        if (not indexLen or (not inCount)):
            return {
                'state': False,
                'reason': '���������������Ϊ�ջ�����ȫ��������Χ'
            }
        # -----��ʼ����ָ����������
        maxIndex = max(indexArray)  # ���������������
        if (maxIndex > dataSum):
            maxIndex = dataSum
        dataArray = [None] * indexLen  # ���ҽ��
        with open(self.path, 'r', encoding=self.encoding) as fl:
            fl.readline()
            curLine = 1
            while (curLine <= maxIndex + 1):
                # ������ҽ��
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

    # ����ָ�����ݵ���������(������1��ʼ�������ڷ���-1)
    # ����{data1:[],data2:[]}
    @tryFunc
    def findDatas(self, dataArray):
        dataLen = len(dataArray)
        # ----����Ϊ��
        if (not dataLen):
            return {
                'state': False,
                'reason': '���������������Ϊ��'
            }
        dataSum = self.getDataSum()['data']
        indexDict = {data: [-1] for data in dataArray}  # ����ֵ�
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

    # ����ָ�����ݵ�һ�����ݵ�����(������1��ʼ�������ڷ���-1)
    # ��������ϵ��
    @tryFunc
    def findOneData(self, data):
        return {
            'state': True,
            'data': self.findDatas([data])['data'][data]
        }

    # ------------------------------��
    # �޸�ָ������������(������1��ʼ)
    # dataDict = {index1:'new1',index2:'new2'}
    @tryFunc
    def modifyIndexData(self, dataDict):
        # �˳�������Χ������
        dataSum = self.getDataSum()['data']
        dataDict = {key: value for key, value in dataDict.items()
                    if key > 0 and key <= dataSum}
        minIndex = min([index for index in dataDict.keys()])
        # ��ʼ�޸�
        modifyDict = {}  # �޸�ϸ��
        with open(self.path, 'r', encoding=self.encoding) as oldFile:
            with open(self.path, 'r+', encoding=self.encoding) as newFile:
                curLine = 0
                # oldFile��λ���޸�������
                while (curLine < minIndex):
                    oldFile.readline()
                    curLine += 1
                # newFileͬ����λ
                newFile.seek(oldFile.tell() - 1)
                # ��ָ���������ݽ����޸�
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

    # �޸�ָ�����ݵ�����
    # dataDict = {'old':'new1','old2':'new2'}
    @tryFunc
    def modifyDatas(self, dataDict):
        modifyDict = {}
        # ��ʼ�޸�
        with open(self.path, 'r', encoding=self.encoding) as oldFile:
            with open(self.path, 'r+', encoding=self.encoding) as newFile:
                oldFile.readline()
                curLine = 1
                # newFile��λ����һ����������
                newFile.seek(oldFile.tell() - 1, 0)
                # �޸�����ָ�����ݵ�����
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

    # ------------------------------ɾ
    # ɾ��ָ������������(������1��ʼ)
    # ����{index1:data1,index2:data2}
    @tryFunc
    def deleteIndexData(self, indexArray):
        # ����Ϊ��
        if (not len(indexArray)):
            return {
                'state': False,
                'reason': '����ɾ����������Ϊ��'
            }
        # �˳�������Χ����������������
        dataSum = self.getDataSum()['data']
        indexArray = [index for index in indexArray if index > 0 and index <= dataSum]
        indexArray.sort()
        # ��ʼɾ��
        deleteDict = {}
        with open(self.path, 'r', encoding=self.encoding) as oldFile:
            with open(self.path, 'r+', encoding=self.encoding) as newFile:
                curLine = 0
                # oldFile��λ��ɾ���е�ǰһ��
                while (curLine < indexArray[0]):
                    oldFile.readline()
                    curLine += 1
                # newFileͬ����λ
                newFile.seek(oldFile.tell() - 1, 0)
                # ��ɾ�������������д��
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

    # ɾ��һ��ָ�����ݵ���������
    # ����ɾ����������
    @tryFunc
    def deleteOneData(self, data):
        index = self.findOneData(data)['data']
        self.deleteIndexData(index)

        return {
            'state': True,
            'msg': index
        }

    # ɾ��ָ�����ݵ���������
    # ����{data1:[index1],data2:[index2]}
    @tryFunc
    def deleteDatas(self, dataArray):
        # ����Ϊ��
        if (not len(dataArray)):
            return {
                'state': False,
                'reason': '����ɾ����������Ϊ��'
            }
        # ��ʼɾ��
        count = 0
        deleteDict = {}  # ɾ��ϸ��
        with open(self.path, 'r', encoding=self.encoding) as oldFile:
            with open(self.path, 'r+', encoding=self.encoding) as newFile:
                oldFile.readline()
                newFile.seek(oldFile.tell() - 1, 0)
                curLine = 1
                nextLine = oldFile.readline()
                curLine += 1
                # ��ɾ���������������д��
                while (nextLine):
                    data = nextLine[1:].rstrip('\n')
                    if (data not in dataArray):
                        newFile.write(nextLine)
                    else:
                        # ����ɾ��ϸ��
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

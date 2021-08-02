# -*- coding: GB2312 -*-

import os
import winreg
from collections import Counter
from mutagen import File
from PyQt5 import QtWidgets


# ---------------------------------------装饰器

# 捕获异常弹出弹窗(DataManager，SetingWindow,SrcViewer专用)
# 1.在class调用函数之后self.errMsg有内容就弹出错误信息弹窗
# 2.在class调用函数之后抛错了就弹出错误信息弹窗
def errMsgBox(func):
    def decorator(self, *args, **kw):
        try:
            res = func(self, *args, **kw)
            if (not self.errMsg == ''):
                QtWidgets.QMessageBox.information(
                    self,
                    "警告",
                    "\n错误信息:{}\n".format(self.errMsg)
                )
            self.errMsg = ''
            return res
        except Exception as err:
            QtWidgets.QMessageBox.warning(
                self,
                "警告",
                "\n错误信息:{}\n".format(err)
            )

    return decorator

    # ---------------------------------------回调函数


# 检查txtDb方法的返回state(DataManager，SetingWindow,SrcViewer专用)
# 1.一般由别的函数间接调用，便于批量捕获异常
# 2.成功返回数据，失败捕获异常并返回默认返回
def dbStateCheck(self, _dbFunc, errReturn=None, _args=[]):
    response = _dbFunc(*_args)
    if (response['state']):
        if ('data' in response.keys()):
            return response['data']
        else:
            return response['msg']
    else:
        # 捕获异常返回默认返回
        if (response['reason'] == "'data'"):
            self.errMsg = self.errMsg + "\n操作数据时，数据库同步出错"
        else:
            self.errMsg = self.errMsg + "\n" + response['reason']
        return errReturn


# 重复文件夹路径处理(加数字)
def repeatDirPathHandle(oldPath):
    num = 1
    newPath = oldPath
    while (os.path.exists(newPath)):
        newPath = '{}_{}'.format(oldPath, num)
        num = num + 1
    return newPath


def repeatFilePathHandle(oldPath):
    num = 1
    name, ext = os.path.splitext(oldPath)
    newPath = oldPath
    while (os.path.exists(newPath)):
        newPath = '{}_{}{}'.format(name, num, ext)
        num = num + 1
    return newPath


# 检查配置文件是否完整存在
# 完整存在：{'state': True,'msg': 0}
# 不存在：{'state': True,'msg': 1}
# 存在但不完整：{'state': True,'msg': 2}
def fileAllExists(baseDir, fileList):
    if (not os.path.exists(baseDir)):
        return {
            'state': False,
            'msg': 1
        }
    for file in fileList:
        path = baseDir + file
        if (not os.path.exists(path)):
            return {
                'state': False,
                'msg': 2
            }
    return {
        'state': True,
        'msg': 0
    }


# 从注册表搜索指定浏览器的路径(不存在返回空字符串)
# mainkey注册表主键值
# subkey注册表局部键值
def findBrowserPath(subkey, mainkey=winreg.HKEY_LOCAL_MACHINE):
    try:
        key = winreg.OpenKey(mainkey, subkey)
    except FileNotFoundError:
        return ''
    value, type = winreg.QueryValueEx(key, "")  # 获取默认值
    return value.split(',')[0]


# 找出列表重复的数据和索引列表(返回字典,索引从0开始)
def repeatCount(array):
    res = dict(Counter(array))
    tmp = {key: value for key, value in res.items() if value > 1}
    res = {key: [] for key, value in tmp.items()}  # 结果字典
    # 查找索引
    for key, value in tmp.items():
        count = value
        for index, data in enumerate(array):
            if (key == data):
                res[key].append(index)
                count -= 1
            if (not count):
                break
    return res


# 提取歌曲信息
def getMusicInfo(path):
    if os.path.exists(path):
        afile = File(path)
        try:
            title = afile.tags['TIT2']
        except Exception as err:
            title = ''
        try:
            artist = afile.tags['TPE1']
        except Exception as err:
            artist = ''
        try:
            cover = afile.tags['APIC:']
            coverData = cover.data
            coverExt = cover.mime.split('/')[-1]
        except Exception as err:
            coverData = ''
            coverExt = ''
        return {
            'title': title,
            'artist': artist,
            'cover': {
                'data': coverData,
                'ext': coverExt
            }
        }

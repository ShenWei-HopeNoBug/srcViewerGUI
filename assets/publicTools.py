# -*- coding: GB2312 -*-

import os
from collections import Counter
from PyQt5 import QtWidgets


# ---------------------------------------װ����

# �����쳣��������(DataManager��SetingWindow,SrcViewerר��)
# 1.��class���ú���֮��self.errMsg�����ݾ͵���������Ϣ����
# 2.��class���ú���֮���״��˾͵���������Ϣ����
def errMsgBox(func):
    def decorator(self, *args, **kw):
        try:
            res = func(self, *args, **kw)
            if (not self.errMsg == ''):
                QtWidgets.QMessageBox.information(
                    self,
                    "����",
                    "\n������Ϣ:{}\n".format(self.errMsg)
                )
            self.errMsg = ''
            return res
        except Exception as err:
            QtWidgets.QMessageBox.warning(
                self,
                "����",
                "\n������Ϣ:{}\n".format(err)
            )

    return decorator

    # ---------------------------------------�ص�����


# ���txtDb�����ķ���state(DataManager��SetingWindow,SrcViewerר��)
# 1.һ���ɱ�ĺ�����ӵ��ã��������������쳣
# 2.�ɹ��������ݣ�ʧ�ܲ����쳣������Ĭ�Ϸ���
def dbStateCheck(self, _dbFunc, errReturn=None, _args=[]):
    response = _dbFunc(*_args)
    if (response['state']):
        if ('data' in response.keys()):
            return response['data']
        else:
            return response['msg']
    else:
        # �����쳣����Ĭ�Ϸ���
        if (response['reason'] == "'data'"):
            self.errMsg = self.errMsg + "\n��������ʱ�����ݿ�ͬ������"
        else:
            self.errMsg = self.errMsg + "\n" + response['reason']
        return errReturn


# �ظ��ļ���·������(������)
def repeatDirPathHandle(oldPath):
    num = 1
    newPath = oldPath
    while (os.path.exists(newPath)):
        newPath = '{}_{}'.format(oldPath, num)
        num = num + 1
    return newPath


# ��������ļ��Ƿ���������
# �������ڣ�{'state': True,'msg': 0}
# �����ڣ�{'state': True,'msg': 1}
# ���ڵ���������{'state': True,'msg': 2}
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


# �ҳ��б��ظ������ݺ������б�(�����ֵ�,������0��ʼ)
def repeatCount(array):
    res = dict(Counter(array))
    tmp = {key: value for key, value in res.items() if value > 1}
    res = {key: [] for key, value in tmp.items()}  # ����ֵ�
    # ��������
    for key, value in tmp.items():
        count = value
        for index, data in enumerate(array):
            if (key == data):
                res[key].append(index)
                count -= 1
            if (not count):
                break
    return res

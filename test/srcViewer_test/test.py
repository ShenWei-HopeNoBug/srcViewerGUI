# -*- coding: GB2312 -*-

import sys
import os
from assets.srcViewer import (
    pathDetection,
    getSortPathList
)


# ���������ļ���
def makeTestFiles():
    DirTest = [
        r'C:\Users\lenovo\Desktop\test\test1',
        r'C:\Users\lenovo\Desktop\test\test2',
        r'C:\Users\lenovo\Desktop\test\test10',
        r'C:\Users\lenovo\Desktop\test\test11',
        r'C:\Users\lenovo\Desktop\test\test21',
    ]
    fileTest = [
        [
            r'\file{}-1.txt'.format(index + 1),
            r'\file{}-2.txt'.format(index + 1),
            r'\file{}-10.txt'.format(index + 1),
        ]
        for index in range(len(DirTest))
    ]
    for index, rootDir in enumerate(DirTest):
        if not os.path.exists(rootDir):
            os.makedirs(rootDir)
        for file in fileTest[index]:
            path = rootDir + file
            if not os.path.exists(path):
                open(path, 'w', encoding='GB2312')
    print('----->>�����ļ��д����ɹ���')


if __name__ == '__main__':
    # ------------------���������ļ���
    makeTestFiles()
    pathList = [
        r'C:\Users\lenovo\Desktop/test',
        r'C:\Users\lenovo\Desktop\test\test21',
        r'C:\Users\lenovo\Desktop\test\����',
        r'G:\��Ƶ\��������',
        r'hahah'
    ]
    pathIgnore = [
        r'C:\Users\lenovo\Desktop\test\test1',
        r'C:\Users\lenovo\Desktop\test\test11',
    ]
    pathList = [os.path.abspath(path) for path in pathList]
    pathIgnore = [os.path.abspath(path) for path in pathIgnore]

    pathList = pathDetection(pathList)
    print('>>�����ļ��У�')
    for path in pathList:
        print(path)
    print('----->��ʼ����')
    sizeOption = {
            'range': [0, 4],
            # 'addSign': 0,
            # 'signChar': ''
        }
    res = getSortPathList(
        pathList,
        pathIgnore,
        ['.txt', '.mp4'],
        ['.xls'],
        sizeOption
    )
    print('>>�ļ���')
    for path in res:
        print(path)
    sys.exit(0)

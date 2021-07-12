# -*- coding: GB2312 -*-

import sys
import os
from assets.srcViewer import (
    pathDetection,
    getSortPathList
)


# 创建测试文件夹
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
    print('----->>测试文件夹创建成功！')


if __name__ == '__main__':
    # ------------------创建测试文件集
    makeTestFiles()
    pathList = [
        r'C:\Users\lenovo\Desktop\test',
        r'C:\Users\lenovo\Desktop\test\test21',
        r'C:\Users\lenovo\Desktop\test\哈哈',
        r'G:\视频\憨豆先生',
    ]
    pathIgnore = [
        r'C:\Users\lenovo\Desktop\test\test1',
        r'C:\Users\lenovo\Desktop\test\test11',
    ]
    pathList = pathDetection(pathList)
    print('>>搜索文件夹：')
    for path in pathList:
        print(path)
    print('----->开始搜索')
    res = getSortPathList(
        pathList,
        pathIgnore,
        ['.txt', '.mp4'],
        ['.xls'],
        [0, 100]
    )
    print('>>文件：')
    for path in res:
        print(path, '---大小{}'.format(os.path.getsize(path)))
    sys.exit(0)

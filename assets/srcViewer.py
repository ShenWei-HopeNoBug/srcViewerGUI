# -*- coding: GB2312 -*-

import os


# ------------去除被包含的路径和重名的路径
# 注意：相同的字符输入法输入字体不一样可能会判断为不同
def pathDetection(pathList):
    # 将右斜杠的路径转换成左斜杠
    pathList = [path.replace('\\', '/') for path in pathList]
    oldPathList = pathList
    # 去重并按字符串长度从小到大排序
    pathList = list(set(pathList))
    pathList = sorted(pathList, key=lambda i: len(i), reverse=True)

    newPathList = []  # 保留的路径
    # 去除被包含的路径
    while pathList:
        newPathList.append(pathList[-1])  # 取出待比较路径
        compStr = pathList.pop().split('/')
        compLen = len(compStr)

        removeList = []  # 本次比较要删除的路径

        deleteflg = True  # 删除标志（True删除False保留）
        for path in pathList:
            keywords = path.split('/')
            # 长度相同不进行比较
            if len(keywords) <= compLen:
                continue
            for index, value in enumerate(compStr):
                if not value == keywords[index]:
                    deleteflg = False
                    break
            if deleteflg:
                removeList.append(path)
        # 删除被包含的路径
        for path in removeList:
            pathList.remove(path)

    # 按原来输入路径的索引升序排序
    newPathList = sorted(newPathList, key=lambda i: oldPathList.index(i), reverse=False)
    return newPathList


# ------------提取搜索根目录下筛选文件地址序列
# dirList：扫描根目录路径序列
# dirIgnore：忽略文件夹根目录序列
# extIgnore：指定要忽略的文件的扩展名
# extList：指定要操作的文件的扩展名
def getSortPathList(dirList, dirIgnore=[], extList=[], extIgnore=[]):
    filePathList = []
    dirIgnoreSet = set()  # 忽略文件夹集合
    # 扫描忽略文件文件夹根目录
    for path in dirIgnore:
        ignorefiles = os.walk(path)
        for root, dirs, files in ignorefiles:
            dirIgnoreSet.add(root)

    # 扫描所有文件
    while dirList:
        dirRoot = os.walk(dirList.pop(0))
        for root, dirs, files in dirRoot:
            if root in dirIgnoreSet:
                continue
            if extIgnore and extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore and
                         os.path.splitext(file)[-1] in extList
                         ]
            # 把要忽略的文件去除
            elif extIgnore:
                files = [file for file in files if os.path.splitext(file)[-1] not in extIgnore]

            # 把指定的文件类型筛选出来
            elif extList:
                files = [file for file in files if os.path.splitext(file)[-1] in extList]

            path = ['{}\\{}'.format(root, file) for file in files]
            filePathList.extend(path)
    return filePathList


# 把路径写入JS文件中'GB2312'
def writePathTojs(pathList, path):
    pathList = [r'"{}",'.format(path).replace('\\', '/') for path in pathList]
    data = r'const pathList=[{}];'.format('\n'.join(pathList))
    with open(path, 'w', encoding='GB2312') as fl:
        fl.write(data)


# 把显示信息写入JS文件中'GB2312'
def writeShowTojs(path, maxRow=3, startPage=1, model=1):
    listType = 'image'
    if model == 2:
        listType = 'video'
    data = 'const maxRow={};\nconst listType="{}";\nlet page={};'.format(maxRow, listType, startPage)
    with open(path, 'w', encoding='GB2312') as fl:
        fl.write(data)

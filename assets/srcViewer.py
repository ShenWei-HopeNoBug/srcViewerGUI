# -*- coding: GB2312 -*-

import os


# ------------去除被包含的路径和重名的路径(输入\\的绝对路径)
# 注意：相同的字符输入法输入字体不一样可能会判断为不同
def pathDetection(pathList):
    # 将左斜杠的路径转换成右斜杠
    oldPathList = pathList
    # 去重并按字符串长度从小到大排序
    pathList = list(set(pathList))
    pathList = [path for path in pathList if os.path.exists(path)]  # 去除不存在的文件夹路径
    pathList = sorted(pathList, key=lambda i: len(i), reverse=True)

    newPathList = []  # 保留的路径
    # 去除被包含的路径
    while pathList:
        newPathList.append(pathList[-1])  # 取出待比较路径
        compStr = pathList.pop().split('\\')
        compLen = len(compStr)

        removeList = []  # 本次比较要删除的路径

        deleteflg = True  # 删除标志（True删除False保留）
        for path in pathList:
            keywords = path.split('\\')
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


# ------------提取搜索根目录下筛选文件地址序列(输入\\的绝对路径)
# dirList：扫描根目录路径序列
# dirIgnore：忽略文件夹根目录序列
# extIgnore：指定要忽略的文件的扩展名
# extList：指定要操作的文件的扩展名
# sizeOption：指定筛选文件大小和超出范围是否写入默认路径(0：不写入，1：写入)
def getSortPathList(dirList, dirIgnore=[], extList=[], extIgnore=[],
                    sizeOption=[0, 4, 1], outChar='#'):
    # 去除不存在的文件夹路径
    dirList = [path for path in dirList if os.path.exists(path)]
    if dirIgnore:
        dirIgnore = [path for path in dirIgnore if os.path.exists(path)]
    # 在超出大小的路径前加的字符是否为空
    if not outChar:
        sizeOption[2] = 0
    filePathList = []  # 保存结果
    # 扫描所有文件
    while dirList:
        dirRoot = os.walk(dirList.pop(0))
        for root, dirs, files in dirRoot:
            if root in dirIgnore:
                continue
            # 去除忽略的文件夹
            dirs = [path for path in dirs
                    if os.path.join(root, path) not in dirIgnore]
            if extIgnore and extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore and
                         os.path.splitext(file)[-1] in extList
                         ]
            # 把要忽略的文件去除
            elif extIgnore:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore]

            # 把指定的文件类型筛选出来
            elif extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] in extList]

            # 拼接路径和筛选大小
            for file in files:
                path = os.path.join(root, file)
                fileSize = os.path.getsize(path) / float(1024 * 1024)
                if (fileSize <= sizeOption[1] and fileSize >= sizeOption[0]):
                    filePathList.append(path)
                elif (sizeOption[2]):
                    filePathList.append('{}{}'.format(outChar, path))

    return filePathList


# 把路径写入JS文件中'GB2312'
def writePathTojs(pathList, path):
    pathList = ['"{}",'.format(path).replace('\\', '/') for path in pathList]
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

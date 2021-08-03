# -*- coding: GB2312 -*-

import os
import re
# 按windows文件名排序方式排序
from natsort import ns, natsorted
from assets.txtDataBase import TxtDatabase
from assets.publicTools import getMusicInfo, repeatFilePathHandle


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
# sizeOption：
#   range指定筛选文件大小
#   addSign超出范围是否添加标记(0：不写入，1：写入)
#   signChar标记字符
def getSortPathList(dirList=[], dirIgnore=[], extList=[], extIgnore=[],
                    sizeOption={}):
    sizeOptionDefault = {
        'range': [0, 10240],
        'addSign': 1,
        'signChar': '#'
    }
    # 用默认配置补全未配置的sizeOption
    sizeOptionKeys = sizeOption.keys()
    if len(sizeOptionKeys):
        for key in sizeOptionDefault.keys():
            if key not in sizeOptionKeys:
                sizeOption[key] = sizeOptionDefault[key]
    else:
        sizeOption = sizeOptionDefault
    # 在超出大小的路径前加的字符是否为空
    if not sizeOption['signChar']:
        sizeOption['signChar'] = sizeOptionDefault['signChar']
    # 去除不存在的文件夹路径
    if dirList:
        dirList = [path for path in dirList if os.path.exists(path)]
    if dirIgnore:
        dirIgnore = [path for path in dirIgnore if os.path.exists(path)]
    # 扫描所有文件
    filePathList = []  # 保存结果
    while dirList:
        dirRoot = os.walk(dirList.pop(0))
        for root, dirs, files in dirRoot:
            if root in dirIgnore:
                continue
            # 去除忽略的文件夹
            dirs = [path for path in dirs
                    if os.path.join(root, path) not in dirIgnore]
            dirs = natsorted(dirs, alg=ns.PATH)  # 按windows风格排序

            # 既有忽略的扩展名又有筛选的扩展名
            if extIgnore and extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore and
                         os.path.splitext(file)[-1] in extList
                         ]
            # 忽略扩展名
            elif extIgnore:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore]

            # 筛选扩展名
            elif extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] in extList]

            files = natsorted(files, alg=ns.PATH)  # 按windows风格排序
            # 拼接路径和筛选大小
            for file in files:
                path = os.path.join(root, file)
                fileSize = os.path.getsize(path) / float(1024 * 1024)
                if fileSize <= sizeOption['range'][1] and fileSize >= sizeOption['range'][0]:
                    filePathList.append(path)
                elif sizeOption['addSign']:
                    filePathList.append('{}{}'.format(sizeOption['signChar'], path))

    return filePathList


# 把路径写入JS文件中'GB18030'
def writePathTojs(pathList, savPath, initPath, coverDir='/cover', encoding='GB18030'):
    # 换成左斜杠
    pathList = [path.replace('\\', '/') for path in pathList]
    if initPath == '/image':
        pathList = ['"{}",'.format(path) for path in pathList]
        data = 'const imgPath=[{}];'.format('\n'.join(pathList))
    elif initPath == '/video':
        pathList = ['"{}",'.format(path) for path in pathList]
        data = 'const videoPath=[{}];'.format('\n'.join(pathList))
    elif initPath == '/music':
        dataList = []
        exg = re.compile(r'[/:*?\\<>"]')  # 处理特殊字符正则对象
        for path in pathList:
            tmpPath = path
            # 大小超范围
            if (path[0] == '#'):
                tmpPath = tmpPath[1:]
            infoDict = getMusicInfo(tmpPath)
            title, artist, cover = infoDict['title'], infoDict['artist'], infoDict['cover']
            # 没有名字用文件名
            if not title:
                file = tmpPath.split('/')[-1]
                title = os.path.splitext(file)[0]
            # 有封面保存封面
            coverUrl = ''
            if cover['data']:
                imgTitle = exg.sub('', title)  # 去除解析文件名中的敏感字符
                imgPath = '{}/{}.{}'.format(coverDir, imgTitle, cover['ext'])
                # 处理重名文件
                coverUrl = repeatFilePathHandle(imgPath)
                coverUrl = os.path.abspath(coverUrl).replace('\\', '/')
                with open(coverUrl, 'wb') as img:
                    img.write(cover['data'])
            # 音频信息(将敏感字符'前面加\，防止前端解析失败)
            info = '"path":"{0}","title":"{1}","artist":"{2}","coverUrl":"{3}"'.format(
                path.replace("'", "\\'"),
                title.replace("'", "\\'"),
                artist.replace("'", "\\'"),
                coverUrl.replace("'", "\\'"),
            )
            dataList.append("'{" + info + "}',")  # 拼成JSON字符串
        data = 'const musicPath=[{}];'.format('\n'.join(dataList))
    else:
        return
    with open(savPath, 'w', encoding=encoding) as fl:
        fl.write(data)


# 把显示信息写入JS文件中'GB18030'
def writeShowTojs(savPath, maxRow=3, startPage=1, initPath='/image', encoding='GB18030'):
    # 修改内容字典
    modifyDict = {1: 'const initPath = "{}";'.format(initPath)}
    if initPath == '/image':
        modifyDict[2] = 'const imgPage = {};'.format(startPage)
        modifyDict[3] = 'const imgRow = {};'.format(maxRow)
    elif initPath == '/video':
        modifyDict[4] = 'const videoPage = {};'.format(startPage)
        modifyDict[5] = 'const videoRow = {};'.format(maxRow)
    elif initPath == '/music':
        modifyDict[6] = 'const musicPage = {};'.format(startPage)
        modifyDict[7] = 'const musicRow = {};'.format(maxRow)
    else:
        return
    # 实例化txtDb
    txtDb = TxtDatabase(savPath)
    txtDb.encoding = encoding
    # 格式化js文件为txtDb格式
    txtDb.initTxtDb()
    txtDb.modifyIndexData(modifyDict)
    # 转回普通js文件
    txtDb.fallback()

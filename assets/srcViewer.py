# -*- coding: GB2312 -*-

import os
import re
# ��windows�ļ�������ʽ����
from natsort import ns, natsorted
from assets.txtDataBase import TxtDatabase
from assets.publicTools import getMusicInfo, repeatFilePathHandle


# ------------ȥ����������·����������·��(����\\�ľ���·��)
# ע�⣺��ͬ���ַ����뷨�������岻һ�����ܻ��ж�Ϊ��ͬ
def pathDetection(pathList):
    # ����б�ܵ�·��ת������б��
    oldPathList = pathList
    # ȥ�ز����ַ������ȴ�С��������
    pathList = list(set(pathList))
    pathList = [path for path in pathList if os.path.exists(path)]  # ȥ�������ڵ��ļ���·��
    pathList = sorted(pathList, key=lambda i: len(i), reverse=True)

    newPathList = []  # ������·��
    # ȥ����������·��
    while pathList:
        newPathList.append(pathList[-1])  # ȡ�����Ƚ�·��
        compStr = pathList.pop().split('\\')
        compLen = len(compStr)

        removeList = []  # ���αȽ�Ҫɾ����·��

        deleteflg = True  # ɾ����־��Trueɾ��False������
        for path in pathList:
            keywords = path.split('\\')
            # ������ͬ�����бȽ�
            if len(keywords) <= compLen:
                continue
            for index, value in enumerate(compStr):
                if not value == keywords[index]:
                    deleteflg = False
                    break
            if deleteflg:
                removeList.append(path)
        # ɾ����������·��
        for path in removeList:
            pathList.remove(path)

    # ��ԭ������·����������������
    newPathList = sorted(newPathList, key=lambda i: oldPathList.index(i), reverse=False)
    return newPathList


# ------------��ȡ������Ŀ¼��ɸѡ�ļ���ַ����(����\\�ľ���·��)
# dirList��ɨ���Ŀ¼·������
# dirIgnore�������ļ��и�Ŀ¼����
# extIgnore��ָ��Ҫ���Ե��ļ�����չ��
# extList��ָ��Ҫ�������ļ�����չ��
# sizeOption��
#   rangeָ��ɸѡ�ļ���С
#   addSign������Χ�Ƿ���ӱ��(0����д�룬1��д��)
#   signChar����ַ�
def getSortPathList(dirList=[], dirIgnore=[], extList=[], extIgnore=[],
                    sizeOption={}):
    sizeOptionDefault = {
        'range': [0, 10240],
        'addSign': 1,
        'signChar': '#'
    }
    # ��Ĭ�����ò�ȫδ���õ�sizeOption
    sizeOptionKeys = sizeOption.keys()
    if len(sizeOptionKeys):
        for key in sizeOptionDefault.keys():
            if key not in sizeOptionKeys:
                sizeOption[key] = sizeOptionDefault[key]
    else:
        sizeOption = sizeOptionDefault
    # �ڳ�����С��·��ǰ�ӵ��ַ��Ƿ�Ϊ��
    if not sizeOption['signChar']:
        sizeOption['signChar'] = sizeOptionDefault['signChar']
    # ȥ�������ڵ��ļ���·��
    if dirList:
        dirList = [path for path in dirList if os.path.exists(path)]
    if dirIgnore:
        dirIgnore = [path for path in dirIgnore if os.path.exists(path)]
    # ɨ�������ļ�
    filePathList = []  # ������
    while dirList:
        dirRoot = os.walk(dirList.pop(0))
        for root, dirs, files in dirRoot:
            if root in dirIgnore:
                continue
            # ȥ�����Ե��ļ���
            dirs = [path for path in dirs
                    if os.path.join(root, path) not in dirIgnore]
            dirs = natsorted(dirs, alg=ns.PATH)  # ��windows�������

            # ���к��Ե���չ������ɸѡ����չ��
            if extIgnore and extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore and
                         os.path.splitext(file)[-1] in extList
                         ]
            # ������չ��
            elif extIgnore:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore]

            # ɸѡ��չ��
            elif extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] in extList]

            files = natsorted(files, alg=ns.PATH)  # ��windows�������
            # ƴ��·����ɸѡ��С
            for file in files:
                path = os.path.join(root, file)
                fileSize = os.path.getsize(path) / float(1024 * 1024)
                if fileSize <= sizeOption['range'][1] and fileSize >= sizeOption['range'][0]:
                    filePathList.append(path)
                elif sizeOption['addSign']:
                    filePathList.append('{}{}'.format(sizeOption['signChar'], path))

    return filePathList


# ��·��д��JS�ļ���'GB18030'
def writePathTojs(pathList, savPath, initPath, coverDir='/cover', encoding='GB18030'):
    # ������б��
    pathList = [path.replace('\\', '/') for path in pathList]
    if initPath == '/image':
        pathList = ['"{}",'.format(path) for path in pathList]
        data = 'const imgPath=[{}];'.format('\n'.join(pathList))
    elif initPath == '/video':
        pathList = ['"{}",'.format(path) for path in pathList]
        data = 'const videoPath=[{}];'.format('\n'.join(pathList))
    elif initPath == '/music':
        dataList = []
        exg = re.compile(r'[/:*?\\<>"]')  # ���������ַ��������
        for path in pathList:
            tmpPath = path
            # ��С����Χ
            if (path[0] == '#'):
                tmpPath = tmpPath[1:]
            infoDict = getMusicInfo(tmpPath)
            title, artist, cover = infoDict['title'], infoDict['artist'], infoDict['cover']
            # û���������ļ���
            if not title:
                file = tmpPath.split('/')[-1]
                title = os.path.splitext(file)[0]
            # �з��汣�����
            coverUrl = ''
            if cover['data']:
                imgTitle = exg.sub('', title)  # ȥ�������ļ����е������ַ�
                imgPath = '{}/{}.{}'.format(coverDir, imgTitle, cover['ext'])
                # ���������ļ�
                coverUrl = repeatFilePathHandle(imgPath)
                coverUrl = os.path.abspath(coverUrl).replace('\\', '/')
                with open(coverUrl, 'wb') as img:
                    img.write(cover['data'])
            # ��Ƶ��Ϣ(�������ַ�'ǰ���\����ֹǰ�˽���ʧ��)
            info = '"path":"{0}","title":"{1}","artist":"{2}","coverUrl":"{3}"'.format(
                path.replace("'", "\\'"),
                title.replace("'", "\\'"),
                artist.replace("'", "\\'"),
                coverUrl.replace("'", "\\'"),
            )
            dataList.append("'{" + info + "}',")  # ƴ��JSON�ַ���
        data = 'const musicPath=[{}];'.format('\n'.join(dataList))
    else:
        return
    with open(savPath, 'w', encoding=encoding) as fl:
        fl.write(data)


# ����ʾ��Ϣд��JS�ļ���'GB18030'
def writeShowTojs(savPath, maxRow=3, startPage=1, initPath='/image', encoding='GB18030'):
    # �޸������ֵ�
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
    # ʵ����txtDb
    txtDb = TxtDatabase(savPath)
    txtDb.encoding = encoding
    # ��ʽ��js�ļ�ΪtxtDb��ʽ
    txtDb.initTxtDb()
    txtDb.modifyIndexData(modifyDict)
    # ת����ͨjs�ļ�
    txtDb.fallback()

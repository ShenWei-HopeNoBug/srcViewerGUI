# -*- coding: GB2312 -*-

import os


# ------------ȥ����������·����������·��
# ע�⣺��ͬ���ַ����뷨�������岻һ�����ܻ��ж�Ϊ��ͬ
def pathDetection(pathList):
    # ����б�ܵ�·��ת������б��
    pathList = [path.replace('\\', '/') for path in pathList]
    oldPathList = pathList
    # ȥ�ز����ַ������ȴ�С��������
    pathList = list(set(pathList))
    pathList = sorted(pathList, key=lambda i: len(i), reverse=True)

    newPathList = []  # ������·��
    # ȥ����������·��
    while pathList:
        newPathList.append(pathList[-1])  # ȡ�����Ƚ�·��
        compStr = pathList.pop().split('/')
        compLen = len(compStr)

        removeList = []  # ���αȽ�Ҫɾ����·��

        deleteflg = True  # ɾ����־��Trueɾ��False������
        for path in pathList:
            keywords = path.split('/')
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


# ------------��ȡ������Ŀ¼��ɸѡ�ļ���ַ����
# dirList��ɨ���Ŀ¼·������
# dirIgnore�������ļ��и�Ŀ¼����
# extIgnore��ָ��Ҫ���Ե��ļ�����չ��
# extList��ָ��Ҫ�������ļ�����չ��
def getSortPathList(dirList, dirIgnore=[], extList=[], extIgnore=[]):
    filePathList = []
    dirIgnoreSet = set()  # �����ļ��м���
    # ɨ������ļ��ļ��и�Ŀ¼
    for path in dirIgnore:
        ignorefiles = os.walk(path)
        for root, dirs, files in ignorefiles:
            dirIgnoreSet.add(root)

    # ɨ�������ļ�
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
            # ��Ҫ���Ե��ļ�ȥ��
            elif extIgnore:
                files = [file for file in files if os.path.splitext(file)[-1] not in extIgnore]

            # ��ָ�����ļ�����ɸѡ����
            elif extList:
                files = [file for file in files if os.path.splitext(file)[-1] in extList]

            path = ['{}\\{}'.format(root, file) for file in files]
            filePathList.extend(path)
    return filePathList


# ��·��д��JS�ļ���'GB2312'
def writePathTojs(pathList, path):
    pathList = [r'"{}",'.format(path).replace('\\', '/') for path in pathList]
    data = r'const pathList=[{}];'.format('\n'.join(pathList))
    with open(path, 'w', encoding='GB2312') as fl:
        fl.write(data)


# ����ʾ��Ϣд��JS�ļ���'GB2312'
def writeShowTojs(path, maxRow=3, startPage=1, model=1):
    listType = 'image'
    if model == 2:
        listType = 'video'
    data = 'const maxRow={};\nconst listType="{}";\nlet page={};'.format(maxRow, listType, startPage)
    with open(path, 'w', encoding='GB2312') as fl:
        fl.write(data)

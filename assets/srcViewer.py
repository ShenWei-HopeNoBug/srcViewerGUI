# -*- coding: GB2312 -*-

import os


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
# sizeOption��ָ��ɸѡ�ļ���С�ͳ�����Χ�Ƿ�д��Ĭ��·��(0����д�룬1��д��)
def getSortPathList(dirList, dirIgnore=[], extList=[], extIgnore=[],
                    sizeOption=[0, 4, 1], outChar='#'):
    # ȥ�������ڵ��ļ���·��
    dirList = [path for path in dirList if os.path.exists(path)]
    if dirIgnore:
        dirIgnore = [path for path in dirIgnore if os.path.exists(path)]
    # �ڳ�����С��·��ǰ�ӵ��ַ��Ƿ�Ϊ��
    if not outChar:
        sizeOption[2] = 0
    filePathList = []  # ������
    # ɨ�������ļ�
    while dirList:
        dirRoot = os.walk(dirList.pop(0))
        for root, dirs, files in dirRoot:
            if root in dirIgnore:
                continue
            # ȥ�����Ե��ļ���
            dirs = [path for path in dirs
                    if os.path.join(root, path) not in dirIgnore]
            if extIgnore and extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore and
                         os.path.splitext(file)[-1] in extList
                         ]
            # ��Ҫ���Ե��ļ�ȥ��
            elif extIgnore:
                files = [file for file in files
                         if os.path.splitext(file)[-1] not in extIgnore]

            # ��ָ�����ļ�����ɸѡ����
            elif extList:
                files = [file for file in files
                         if os.path.splitext(file)[-1] in extList]

            # ƴ��·����ɸѡ��С
            for file in files:
                path = os.path.join(root, file)
                fileSize = os.path.getsize(path) / float(1024 * 1024)
                if (fileSize <= sizeOption[1] and fileSize >= sizeOption[0]):
                    filePathList.append(path)
                elif (sizeOption[2]):
                    filePathList.append('{}{}'.format(outChar, path))

    return filePathList


# ��·��д��JS�ļ���'GB2312'
def writePathTojs(pathList, path):
    pathList = ['"{}",'.format(path).replace('\\', '/') for path in pathList]
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

import sys
from assets.srcViewer import (
    pathDetection,
    getFileName
)

if __name__ == '__main__':
    pathList = [
        r'C:\Users\lenovo\Desktop\test\file10',
        r'C:\Users\lenovo\Desktop\test\file1',
        r'C:\Users\lenovo\Desktop\test\file21',
    ]
    pathList = pathDetection(pathList)
    print('搜索文件夹：')
    for path in pathList:
        print(path)
    print('--------------------------------')
    res = getFileName(pathList, [], ['.txt', '.xls'], ['.xls'])
    print('文件：')
    for path in res:
        print(path)
    sys.exit(0)

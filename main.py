# -*- coding: GB2312 -*-

import sys
from PyQt5 import QtWidgets
from windowUi.mainWindow.mainWindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # 数据库
    rootDir = './seting'
    setingName = 'default'
    dbPathList = [
        '/DirList.txt',
        '/DirIgnore.txt',
        '/ExtList.txt',
        '/ExtIgnore.txt',
        '/OtherSeting.txt',
    ]
    # 主窗口
    mainWin = MainWindow(rootDir, setingName, dbPathList)
    mainWin.show()
    sys.exit(app.exec_())

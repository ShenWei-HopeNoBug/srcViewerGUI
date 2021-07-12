# -*- coding: GB2312 -*-

import sys
from PyQt5 import QtWidgets
from windowUi.mainWindow.mainWindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # ���ݿ�
    rootDir = './seting'
    setingName = 'default'
    dbPathList = [
        '/DirList.txt',
        '/DirIgnore.txt',
        '/ExtList.txt',
        '/ExtIgnore.txt',
        '/OtherSeting.txt',
    ]
    # ������
    mainWin = MainWindow(rootDir, setingName, dbPathList)
    mainWin.show()
    sys.exit(app.exec_())

import sys
from PyQt5 import QtWidgets
from windowUi.setingWindow.setingWindow import SetingWindow
from assets.txtDataBase import TxtDatabase

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 数据库
    dbBaseDir = './seting'
    dbPathList = [
        '/DirList.txt',
        '/DirIgnore.txt',
        '/ExtList.txt',
        '/ExtIgnore.txt',
        '/OtherSeting.txt',
    ]
    initData = [
        ['H:/N2相关', 'H:/前端'],
        ['H:/python程序'],
        ['.png', '.jpg'],
        ['.gif'],
        ['3', '1', '1'],
    ]
    txtDb = TxtDatabase(dbPathList[0])
    for index in range(5):
        txtDb.path = dbBaseDir + dbPathList[index]
        txtDb.clearAll()
        txtDb.addDatas(initData[index])
    # 数据管理UI
    myshow = SetingWindow(txtDb, dbBaseDir, dbPathList)
    myshow.show()

    sys.exit(app.exec_())

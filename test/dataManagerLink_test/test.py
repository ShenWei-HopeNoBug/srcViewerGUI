import sys
from PyQt5 import QtWidgets
from assets.txtDataBase import TxtDatabase
from windowUi.dataManager.dataManager import DataManager

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 数据库
    dbPath = './test.txt'
    txtDb = TxtDatabase(dbPath)
    # txtDb.sumCheck()
    txtDb.clearAll()
    txtDb.addDatas([
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine',
        'ten',
        'one'
    ])
    # 数据管理UI
    myshow = DataManager('test', txtDb)
    myshow.show()

    sys.exit(app.exec_())

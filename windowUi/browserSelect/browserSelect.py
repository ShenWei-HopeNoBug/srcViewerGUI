# -*- coding: GB2312 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from .browserSelect_ui import Ui_browserSelect
from assets.publicTools import findBrowserPath


class BrowserSelect(QtWidgets.QDialog, Ui_browserSelect):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.selected = 'default'
        self.browserList = ['default']
        # 初始化Ui
        self.initUi()
        # 单选按钮分组
        self.rbtnGroup = QtWidgets.QButtonGroup(self)
        self.rbtnGroup.addButton(self.rbtnDefault, id=0)
        self.rbtnGroup.addButton(self.rbtnChrome, id=1)
        self.rbtnGroup.addButton(self.rbtnFirefox, id=2)
        self.rbtnGroup.addButton(self.rbtnEdge, id=3)
        # 绑定事件
        self.btnBox.clicked.connect(self._signalSend)
        self.rbtnGroup.buttonClicked.connect(self._browserSelected)

    # 初始化UI
    def initUi(self):
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle('选择框')
        self.setFixedSize(self.width(), self.height())
        # 设置美化样式
        self.setWindowOpacity(0.95)
        winStyle = '''
        #browserSelect{
            background-color:rgb(255, 224, 178);
        }
        '''
        self.setStyleSheet(winStyle)
        # 初始化选择
        self.rbtnDefault.click()
        self.searchPath()
        if (not self.browserList[1]):
            self.rbtnChrome.setDisabled(True)
        if (not self.browserList[2]):
            self.rbtnFirefox.setDisabled(True)
        if (not self.browserList[3]):
            self.rbtnEdge.setDisabled(True)

    def searchPath(self):
        searchList = [
            "SOFTWARE\\Clients\\StartMenuInternet\\Google Chrome\\DefaultIcon",
            "SOFTWARE\\Clients\\StartMenuInternet\\FIREFOX.EXE\\DefaultIcon",
            "SOFTWARE\\Clients\\StartMenuInternet\\Microsoft Edge\\DefaultIcon",
        ]
        for browser in searchList:
            path = findBrowserPath(browser)
            self.browserList.append(path)

    # ----------------------绑定事件
    def _browserSelected(self, rbtn):
        self.selected = self.browserList[self.rbtnGroup.id(rbtn)]

    # 发送信号
    def _signalSend(self, btn):
        # print(btn.text())
        if (btn.text() == 'OK'):
            self._signal.emit(self.selected)

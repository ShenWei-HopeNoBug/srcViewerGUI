# -*- coding: GB2312 -*-
from PyQt5 import QtWidgets
from .setingWindow_ui import Ui_setingWindow
from windowUi.dataManager.dataManager import DataManager
from assets.publicTools import errMsgBox, dbStateCheck
from assets.txtDataBase import TxtDatabase

'''
self.dbPathList 默认值：
[
    '/DirList.txt',
    '/DirIgnore.txt',
    '/ExtList.txt',
    '/ExtIgnore.txt',
    '/OtherSeting.txt',
]
'''


# ************************************设置窗口
class SetingWindow(QtWidgets.QDialog, Ui_setingWindow):
    def __init__(self, dbBaseDir, dbPathList):
        super(SetingWindow, self).__init__()
        self.txtDb = TxtDatabase(dbBaseDir + dbPathList[0])  # 连接txtDb对象
        self.dbBaseDir = dbBaseDir  # txtDb操作路径根目录
        self.dbPathList = dbPathList  # txtDb操作路径子文件名列表
        self.otherSeting = []  # otherSeting配置内容
        self.errMsg = ''  # 错误信息
        self.rbtnGroup = QtWidgets.QButtonGroup(self)  # 单选按钮分组
        self.btnGroup = QtWidgets.QButtonGroup(self)  # 点击按钮分组
        # 初始化UI
        self.initUi()
        # 设置单选按钮分组
        self.rbtnGroup.addButton(self.rbtnImage, id=1)
        self.rbtnGroup.addButton(self.rbtnVideo, id=2)
        # 设置点击按钮分组
        self.btnGroup.addButton(self.btnDirList, id=0)
        self.btnGroup.addButton(self.btnDirIgnore, id=1)
        self.btnGroup.addButton(self.btnExtList, id=2)
        self.btnGroup.addButton(self.btnExtIgnore, id=3)
        # 绑定事件
        self.spinBoxMaxRow.valueChanged.connect(self._maxRowChanged)
        self.spinBoxStartPage.valueChanged.connect(self._startPageChanged)
        self.rbtnGroup.buttonClicked.connect(self._modelChanged)
        self.btnGroup.buttonClicked.connect(self._setingModify)
        self.btnBoxConfirm.clicked.connect(self._savOtherSeting)

    # 初始化UI
    @errMsgBox
    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('修改配置')
        self.titleLabel.setText('配置文件名：{}'.format(self.dbBaseDir.split('/')[-1]))
        # 限制计数器下限
        self.spinBoxMaxRow.setMinimum(1)
        self.spinBoxStartPage.setMinimum(1)
        # 加载配置
        self.loadSeting()

    # ------------------------------基本方法
    # 加载保存的otherSeting配置
    @errMsgBox
    def loadSeting(self):
        # 操作数据库
        self.txtDb.path = self.dbBaseDir + self.dbPathList[4]  # 修改dbtxt路径
        self.otherSeting = dbStateCheck(self, self.txtDb.printDatas, ['3', '1', '1'])
        # 设置计数框
        self.spinBoxMaxRow.setValue(int(self.otherSeting[0]))
        self.spinBoxStartPage.setValue(int(self.otherSeting[1]))
        # 设置单选按钮
        if (self.otherSeting[2] == '1'):
            self.rbtnImage.click()
        else:
            self.rbtnVideo.click()

    # 打开修改配置子窗口
    @errMsgBox
    def openModifyWindow(self, dataName, dbPathIndex):
        dbWorkPath = self.dbBaseDir + self.dbPathList[dbPathIndex]
        modifyWindow = DataManager(dataName, dbWorkPath)
        modifyWindow.exec()

    # ------------------------------绑定事件
    # 保存修改的otherSeting配置并退出
    @errMsgBox
    def _savOtherSeting(self, btn):
        if (btn.text() == 'OK'):
            # 操作数据库
            modifyDict = {index + 1: value for index, value in enumerate(self.otherSeting)}
            self.txtDb.path = self.dbBaseDir + self.dbPathList[4]  # 修改dbtxt路径
            dbStateCheck(self, self.txtDb.modifyIndexData, None, [modifyDict])
        self.close()

    # 单页行数变化
    @errMsgBox
    def _maxRowChanged(self, value):
        self.otherSeting[0] = str(value)

    # 最大行数变化
    @errMsgBox
    def _startPageChanged(self, value):
        self.otherSeting[1] = str(value)

    # 模式变化
    @errMsgBox
    def _modelChanged(self, rbtn):
        # 存储按钮id号
        self.otherSeting[2] = str(self.rbtnGroup.id(rbtn))

    # 根据按钮id打开对应修改窗口
    @errMsgBox
    def _setingModify(self, btn):
        self.openModifyWindow(btn.text(), self.btnGroup.id(btn))

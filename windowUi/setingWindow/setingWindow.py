# -*- coding: GB2312 -*-
from PyQt5 import QtWidgets, QtGui
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
        self.rbtnGroup.addButton(self.rbtnMusic, id=3)
        # 设置点击按钮分组
        self.btnGroup.addButton(self.btnDirList, id=0)
        self.btnGroup.addButton(self.btnDirIgnore, id=1)
        self.btnGroup.addButton(self.btnExtList, id=2)
        self.btnGroup.addButton(self.btnExtIgnore, id=3)
        # 绑定事件
        self.spinBoxMaxRow.valueChanged.connect(self._maxRowChanged)
        self.spinBoxStartPage.valueChanged.connect(self._startPageChanged)
        self.spinBoxSizeMin.valueChanged.connect(self._sizeMinChanged)
        self.spinBoxSizeMax.valueChanged.connect(self._sizeMaxChanged)
        self.checkBoxPlace.stateChanged.connect(self._placeChanged)
        self.rbtnGroup.buttonClicked.connect(self._modelChanged)
        self.btnGroup.buttonClicked.connect(self._setingModify)

    # 初始化UI
    @errMsgBox
    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('修改配置')
        self.titleLabel.setText('配置文件名：{}'.format(self.dbBaseDir.split('/')[-1]))
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setFixedSize(self.width(), self.height())
        # 设置美化样式
        self.setWindowOpacity(0.95)
        winStyle = '''
        #setingWindow{
            background-color:rgb(255, 224, 178);
        }
        
        QSpinBox{
            background-color:rgb(251,232,204)
        }
        
        #btnDirList,
        #btnDirIgnore,
        #btnExtList,
        #btnExtIgnore{
            background-color:rgb(250, 250, 250);
            border-radius:10px;
            border: 1px solid skyblue;
        }
        #btnDirList:hover,
        #btnDirIgnore:hover,
        #btnExtList:hover,
        #btnExtIgnore:hover{
            color:white;
            background-color:rgb(97, 97, 97);
            border-width:0;
            font-size:20px;
        }
        '''
        self.setStyleSheet(winStyle)
        # 限制计数器上下限
        self.spinBoxMaxRow.setMinimum(1)
        self.spinBoxMaxRow.setMaximum(12)
        self.spinBoxStartPage.setMinimum(1)
        self.spinBoxStartPage.setMaximum(9999999)
        self.spinBoxSizeMin.setMinimum(0)
        self.spinBoxSizeMin.setMaximum(10240)
        self.spinBoxSizeMax.setMinimum(1)
        self.spinBoxSizeMax.setMaximum(20480)
        # 加载配置
        self.loadSeting()

    # ------------------------------基本方法
    # 加载保存的otherSeting配置
    @errMsgBox
    def loadSeting(self):
        # 操作数据库
        self.txtDb.path = self.dbBaseDir + self.dbPathList[4]  # 修改dbtxt路径
        self.otherSeting = dbStateCheck(self, self.txtDb.printDatas, ['3', '1', '/image', '0', '10', '0'])
        # 设置计数框
        self.spinBoxMaxRow.setValue(int(self.otherSeting[0]))
        self.spinBoxStartPage.setValue(int(self.otherSeting[1]))
        self.spinBoxSizeMin.setValue(int(self.otherSeting[3]))
        self.spinBoxSizeMax.setValue(int(self.otherSeting[4]))
        # 设置单选按钮
        if (self.otherSeting[2] == '/image'):
            self.rbtnImage.click()
        elif (self.otherSeting[2] == '/video'):
            self.rbtnVideo.click()
        elif (self.otherSeting[2] == '/music'):
            self.rbtnMusic.click()
        # 设置勾选框
        if (int(self.otherSeting[5])):
            self.checkBoxPlace.click()

    # 打开修改配置子窗口
    @errMsgBox
    def openModifyWindow(self, dataName, dbPathIndex):
        dbWorkPath = self.dbBaseDir + self.dbPathList[dbPathIndex]
        modifyWindow = DataManager(dataName, dbWorkPath)
        modifyWindow.exec()

    # 弹出提示框
    def infoBox(self, msg):
        QtWidgets.QMessageBox.information(
            self,
            "提醒",
            msg
        )

    # 弹出询问框
    def questionBox(self, msg):
        return QtWidgets.QMessageBox.question(
            self,
            '询问',
            msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

    # 保存修改的otherSeting配置
    @errMsgBox
    def savOtherSeting(self):
        modifyDict = {index + 1: value for index, value in enumerate(self.otherSeting)}
        # 操作数据库
        self.txtDb.path = self.dbBaseDir + self.dbPathList[4]  # 修改dbtxt路径
        dbStateCheck(self, self.txtDb.modifyIndexData, None, [modifyDict])

    # 关闭窗口确认并保存修改配置
    def closeEvent(self, event):
        if (self.questionBox("修改配置完成？") == QtWidgets.QMessageBox.Yes):
            self.savOtherSeting()
            event.accept()
        else:
            event.ignore()

    # ------------------------------绑定事件
    # 单页行数变化
    @errMsgBox
    def _maxRowChanged(self, value):
        self.otherSeting[0] = str(value)

    # 起始页码变化
    @errMsgBox
    def _startPageChanged(self, value):
        self.otherSeting[1] = str(value)

    # 模式变化
    @errMsgBox
    def _modelChanged(self, rbtn):
        # 存储按钮id号
        id = self.rbtnGroup.id(rbtn)
        if (id == 1):
            self.otherSeting[2] = '/image'
        elif (id == 2):
            self.otherSeting[2] = '/video'
        else:
            self.otherSeting[2] = '/music'

    # 文件大小下限变化
    @errMsgBox
    def _sizeMinChanged(self, value):
        maxSize = self.spinBoxSizeMax.value()
        if (value >= maxSize):
            self.spinBoxSizeMax.setValue(value + 1)
        self.otherSeting[3] = str(value)

    @errMsgBox
    # 文件大小上限变化
    def _sizeMaxChanged(self, value):
        minSize = self.spinBoxSizeMin.value()
        if (value <= minSize):
            self.spinBoxSizeMin.setValue(value - 1)
        self.otherSeting[4] = str(value)

    # 单选框被点击
    @errMsgBox
    def _placeChanged(self, state):
        if (state == 2):
            state = 1
        self.otherSeting[5] = str(state)

    # 根据按钮id打开对应修改窗口
    @errMsgBox
    def _setingModify(self, btn):
        self.openModifyWindow(btn.text(), self.btnGroup.id(btn))

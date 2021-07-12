# -*- coding: GB2312 -*-
import re
from PyQt5 import QtWidgets
from .dataManager_ui import Ui_dataManager
from windowUi.dataInput.dataInput import DataInput
from assets.publicTools import errMsgBox, dbStateCheck
from assets.txtDataBase import TxtDatabase


# ********************************数据管理UI
class DataManager(QtWidgets.QDialog, Ui_dataManager):
    def __init__(self, dataName, dbWorkPath):
        super(DataManager, self).__init__()
        # 实例私有变量
        self.dataName = dataName  # 管理数据名
        self.txtDb = TxtDatabase(dbWorkPath)  # 连接的txt数据库
        self.dataSum = 0  # 数据总数
        self.selectedRow = -1  # 选中listItem的索引(-1代表没选中)
        self.errMsg = ''  # 异常捕获
        self.signData = ''  # 从子窗口接收到的数据
        # 初始化Ui
        self.initUi()
        # 绑定事件
        self.listWidget.itemClicked.connect(self._itemShow)
        self.btnAddData.clicked.connect(self._itemAdd)
        self.btnModifyData.clicked.connect(self._itemModify)
        self.btnDeleteData.clicked.connect(self._itemDelete)
        self.btnClearAll.clicked.connect(self._itemClearAll)

    # ----------------------基本方法
    # 初始化UI
    @errMsgBox
    def initUi(self):
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.dataNameLabel.setText("数据名：{}".format(self.dataName))
        self.setWindowTitle("【{}】数据管理".format(self.dataName))
        # 数据库加载数据
        self.itemLoad()

    # 接收从子窗口传来的数据
    @errMsgBox
    def getSignData(self, signData):
        self.signData = signData

    # ----------------------显示
    # 更新数据总数显示
    @errMsgBox
    def updataDataSumLabel(self):
        self.dataSumLabel.setText("数据量：{}".format(self.dataSum))

    # ----------------------数据相关
    # 从数据库加载列表数据
    @errMsgBox
    def itemLoad(self):
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n数据库路径不存在，加载数据出错'
            return
        # 操作数据库
        self.listWidget.addItems(dbStateCheck(self, self.txtDb.printDatas, []))
        self.dataSum = dbStateCheck(self, self.txtDb.getDataSum, 0)
        self.updataDataSumLabel()

    # ----------------------绑定事件
    # 显示选中项
    @errMsgBox
    def _itemShow(self, item):
        self.dataDetail.clear()
        self.selectedRow = self.listWidget.selectedIndexes()[0].row()
        self.dataDetail.append('数据 {} ：'.format(self.selectedRow + 1))
        self.dataDetail.append(item.text())
        # 滚动条置顶
        self.dataDetail.verticalScrollBar().setValue(0)

    # 清除列表数据
    @errMsgBox
    def _itemClearAll(self, event):
        if (self.dataSum == 0):
            return
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n数据库路径不存在，清空数据出错'
            return
        # 确认弹窗
        reply = QtWidgets.QMessageBox.question(
            self,
            '提醒',
            "\n清空后无法恢复，确认要删除全部数据？\n",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if (reply == QtWidgets.QMessageBox.No):
            return
        # 开始删库
        self.listWidget.clear()
        # 操纵数据库
        dbStateCheck(self, self.txtDb.clearAll)
        # 更新显示
        self.dataDetail.clear()
        self.dataSum = 0
        self.updataDataSumLabel()
        QtWidgets.QMessageBox.information(
            self,
            "提醒",
            "\n数据已全部删除！\n"
        )

    # 删除选中项
    @errMsgBox
    def _itemDelete(self, event):
        if (self.selectedRow == -1):
            QtWidgets.QMessageBox.information(
                self,
                "提醒",
                "\n请选中一条数据后再操作！\n"
            )
            return
        # 删除提醒
        reply = QtWidgets.QMessageBox.question(
            self,
            '提醒',
            "\n确认要删除选中数据？\n",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if (reply == QtWidgets.QMessageBox.No):
            return
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n数据库路径不存在，删除数据出错'
            return
        # 开始删除
        self.listWidget.takeItem(self.selectedRow)
        # 操纵数据库
        dbStateCheck(self, self.txtDb.deleteIndexData, None, [[self.selectedRow + 1]])
        self.selectedRow = -1
        # 更新显示
        self.dataSum -= 1
        self.updataDataSumLabel()
        self.dataDetail.clear()

    # 修改选中项
    @errMsgBox
    def _itemModify(self, event):
        if (self.selectedRow == -1):
            QtWidgets.QMessageBox.information(
                self,
                "提醒",
                "\n请选中一条数据后再操作！\n"
            )
            return
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n数据库路径不存在，修改数据出错'
            return
        self.signData = ''
        oldData = self.listWidget.item(self.selectedRow).text()
        # 打开输入子窗口
        modifyWindow = DataInput(
            self.dataName,
            '【{}】数据修改'.format(self.dataName),
            '请修改数据(不推荐Enter换行、Tab缩进等操作)',
            oldData
        )
        modifyWindow._signal.connect(self.getSignData)
        modifyWindow.exec()
        # 没有输入内容不修改
        newData = self.signData.lstrip('\n').rstrip('\n')
        self.signData = ''
        if (newData == '' or newData == oldData):
            return

        # 修改列表数据
        self.listWidget.takeItem(self.selectedRow)
        self.listWidget.insertItem(self.selectedRow, newData)
        self.listWidget.setCurrentRow(self.selectedRow)
        # 操纵数据库
        dbStateCheck(self,
                     self.txtDb.modifyIndexData,
                     None,
                     [{self.selectedRow + 1: newData}]
                     )
        # 更新显示
        self.dataDetail.clear()
        self.dataDetail.append(newData)

        # 调整提示框显示内容(插入换行符)
        def strLimit(string, limit):
            countLine = len(string) // limit
            string = list(string)
            for index in range(countLine):
                string.insert(limit * (index + 1) + index, '\n')
            return ''.join(string)

        limit = 40  # 单行限制字符数
        oldData = strLimit(oldData, limit)
        newData = strLimit(newData, limit)
        QtWidgets.QMessageBox.information(
            self,
            "提醒",
            "\n数据修改成功！\n原数据：{}\n=>\n新数据：{}".format(oldData, newData)
        )

    # 添加新数据
    @errMsgBox
    def _itemAdd(self, event):
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n数据库路径不存在，添加数据出错'
            return
        self.signData = ''
        # 打开输入子窗口
        inputWindow = DataInput(self.dataName)
        inputWindow._signal.connect(self.getSignData)
        inputWindow.exec()
        # 没有输入内容不修改
        if (self.signData == ''):
            return
        # 接收数据并去回车符
        data = self.signData.lstrip('\n').rstrip('\n')
        data = re.sub(r'\n+', '\n', data)
        data = data.split('\n')
        # 添加数据
        self.listWidget.addItems(data)
        self.dataSum += len(data)
        # 操纵数据库
        dbStateCheck(self, self.txtDb.addDatas, None, [data])
        # 更新显示
        self.listWidget.scrollToBottom()
        self.dataDetail.clear()
        self.selectedRow = -1
        self.updataDataSumLabel()
        self.signData = ''

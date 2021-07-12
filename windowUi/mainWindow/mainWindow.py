# -*- coding: GB2312 -*-

import os
import time
import shutil
import webbrowser
from PyQt5 import QtWidgets
from .mainWindow_ui import Ui_mainWindow
from windowUi.setingWindow.setingWindow import SetingWindow
from assets.publicTools import (
    errMsgBox,
    dbStateCheck,
    repeatDirPathHandle,
    fileAllExists
)
from assets.txtDataBase import TxtDatabase
from assets.srcViewer import (
    pathDetection,
    getSortPathList,
    writePathTojs,
    writeShowTojs
)


class MainWindow(QtWidgets.QWidget, Ui_mainWindow):
    def __init__(self, rootDir, setingName, dbPathList):
        super(MainWindow, self).__init__()
        self.txtDb = TxtDatabase('./config/seting.txt')  # 连接txtDb对象
        self.rootDir = rootDir + '/'  # 设置目录根文件夹
        self.setingName = setingName  # 设置名
        self.dbPathList = dbPathList  # txtDb操作路径子文件名列表
        self.setingSavPath = './config/seting.txt'  # 保存配置文件路径
        self.historySavPath = './config/history.txt'  # 保存历史记录文件路径
        self.errMsg = ''  # 错误信息
        self.selectedRow = -1  # 选中listItem的索引(-1代表没选中)
        self.setingSum = 0  # 设置总数
        self.historySeting = ''  # 设置历史记录
        # 初始化Ui
        self.initUi()
        # 绑定事件
        self.listWidget.itemClicked.connect(self._itemShow)
        self.btnLoadSeting.clicked.connect(self._loadSeting)
        self.btnModifySeting.clicked.connect(self._modifySeting)
        self.btnNewSeting.clicked.connect(self._newSeting)
        self.btnDeleteSeting.clicked.connect(self._deleteSeting)
        self.btnBrowser.clicked.connect(self._openBrowser)

    # 初始化Ui
    @errMsgBox
    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('资源预览v1.0      浙工大机械B406')
        # 检查和新建配置文件
        self.checkDefault()
        # 加载列表和历史记录
        self.itemLoad()
        self.loadHistory()

    # 第一次打开新建默认配置文件
    @errMsgBox
    def checkDefault(self):
        # 检查历史记录文件
        configDir = './config'
        if (not os.path.exists(configDir)):
            os.makedirs(configDir)
        configList = ['/history.txt', '/seting.txt']
        initConfig = [
            ['', 'no'],
            ['default'],
        ]
        for index, flie in enumerate(configList):
            configPath = configDir + flie
            if (not os.path.exists(configPath)):
                self.txtDb.path = configPath
                self.txtDb.clearAll()
                self.txtDb.addDatas(initConfig[index])
        # 检查配置文件
        dbBaseDir = './seting/default'
        if (not os.path.exists(dbBaseDir)):
            os.makedirs(dbBaseDir)
        initData = [
            ['./browser/src'],
            [],
            ['.png', '.jpg', '.gif'],
            [],
            ['3', '1', '1'],
        ]
        for index, flie in enumerate(self.dbPathList):
            setingPath = dbBaseDir + flie
            if (not os.path.exists(setingPath)):
                self.txtDb.path = setingPath
                self.txtDb.clearAll()
                self.txtDb.addDatas(initData[index])

    # ------------------------------基本方法
    # 加载配置列表
    @errMsgBox
    def itemLoad(self):
        if (not os.path.exists(self.setingSavPath)):
            self.errMsg = self.errMsg + '\n配置记录文件路径不存在，加载配置列表失败'
            return
        # 操作数据库
        self.txtDb.path = self.setingSavPath
        self.listWidget.addItems(dbStateCheck(self, self.txtDb.printDatas, []))
        self.setingSum = dbStateCheck(self, self.txtDb.getDataSum, 0)

    # 加载历史记录信息
    @errMsgBox
    def loadHistory(self):
        if (not os.path.exists(self.historySavPath)):
            self.errMsg = self.errMsg + '\n历史记录文件路径不存在，加载历史记录失败'
            return
        # 操作数据库
        self.txtDb.path = self.historySavPath
        historyList = dbStateCheck(self, self.txtDb.printDatas, ['', 'no'])
        # 更新显示
        self.historyLabel.setText('已载入配置：{}'.format(historyList[0]))
        self.historySeting = historyList[0]
        self.updataState(historyList[1])

    # 更新载入历史显示
    @errMsgBox
    def updataState(self, state):
        # 判断状态
        if (self.historySeting == ''):
            self.stateLabel.setText('状态：')
        elif (state == 'yes'):
            self.stateLabel.setText('状态：有修改动作')
        else:
            self.stateLabel.setText('状态：无修改')

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

    # 读取路径配置并写入JS
    def rwPathList(self):
        basePath = self.rootDir + self.setingName
        # 读取路径配置
        pathSetingList = []
        for file in self.dbPathList[0:4]:
            self.txtDb.path = basePath + file
            pathSetingList.append(dbStateCheck(self, self.txtDb.printDatas, []))
        # 去除重复和被包含的路径
        pathSetingList[0] = pathDetection(pathSetingList[0])
        pathSetingList[1] = pathDetection(pathSetingList[1])
        pathSetingList[2] = list(set(pathSetingList[2]))
        pathSetingList[3] = list(set(pathSetingList[3]))
        # 将路径变为绝对路径
        pathSetingList[0] = [os.path.abspath(path) for path in pathSetingList[0]]
        pathSetingList[1] = [os.path.abspath(path) for path in pathSetingList[1]]
        pathList = getSortPathList(*pathSetingList)
        # 写入路径配置
        if (not pathList):
            self.infoBox('\n检索目录无指定文件！\n')
            return False
        writePathTojs(pathList, "./browser/js/pathList.js")
        return True

    # 读取显示配置并写入JS
    def rwShowList(self):
        self.txtDb.path = self.rootDir + self.setingName + self.dbPathList[4]
        showSetingList = dbStateCheck(self, self.txtDb.printDatas, [])
        showSetingList = [int(value) for value in showSetingList]
        # 写入显示配置
        writeShowTojs("./browser/js/options.js", *showSetingList)

    # 关闭窗口确认
    def closeEvent(self, event):
        if (self.questionBox("确认退出？") == QtWidgets.QMessageBox.Yes):
            event.accept()
        else:
            event.ignore()

    # ------------------------------绑定事件
    # 打开浏览器
    @errMsgBox
    def _openBrowser(self, event):
        browserPath = "./browser/html/index.html"
        if (not os.path.exists(browserPath)):
            self.infoBox('\n预览html文件不存在！\n')
        if (self.questionBox('\n是否打开浏览器？\n') == QtWidgets.QMessageBox.Yes):
            webbrowser.open(os.path.abspath(browserPath))

    # 显示选中项
    @errMsgBox
    def _itemShow(self, item):
        self.selectedLabel.setText('已选择配置：{}'.format(item.text()))
        # 保存选中索引和内容
        self.selectedRow = self.listWidget.selectedIndexes()[0].row()
        self.setingName = self.listWidget.item(self.selectedRow).text()

    # 载入选中配置
    @errMsgBox
    def _loadSeting(self, event):
        # 是否选中配置
        if (self.selectedRow == -1):
            self.infoBox("\n请选中某个配置后再操作！\n")
            return
        # 检查选中配置是否完整存在
        if (not fileAllExists(self.rootDir + self.setingName, self.dbPathList)['state']):
            self.infoBox("\n配置【{}】文件不完整！\n".format(self.setingName))
            return
        # -----------------------corn start------------------------
        if (not (self.setingName == self.historySeting)):
            if (not self.rwPathList()):
                return
            self.rwShowList()
        else:
            if (self.questionBox('\n是否重载路径配置\n') == QtWidgets.QMessageBox.Yes):
                if (not self.rwPathList()):
                    return
                self.infoBox('\n载入配置【{}】内路径配置成功\n'.format(self.setingName))
            time.sleep(0.1)
            if (self.questionBox('\n是否重载显示配置\n') == QtWidgets.QMessageBox.Yes):
                self.rwShowList()
                self.infoBox('\n载入配置【{}】内显示配置成功\n'.format(self.setingName))
            self.txtDb.path = self.historySavPath
            # 更新修改状态
            dbStateCheck(
                self,
                self.txtDb.modifyIndexData,
                None,
                [{2: 'no'}]
            )
            self.updataState('no')
            return
        # -----------------------corn end------------------------
        # 操作数据库修改历史记录
        self.txtDb.path = self.historySavPath
        data = self.setingName
        dbStateCheck(
            self,
            self.txtDb.modifyIndexData,
            None,
            [{
                1: data,
                2: 'no'
            }])
        # 更新显示
        self.historySeting = data
        self.historyLabel.setText('已载入配置：{}'.format(self.setingName))
        self.updataState('no')
        self.infoBox('\n载入配置【{}】内路径和显示配置成功\n'.format(self.setingName))

    # 修改选中配置
    @errMsgBox
    def _modifySeting(self, event):
        if (self.selectedRow == -1):
            self.infoBox("\n请选中某个配置后再操作！\n")
            return
        # 打开配置窗口
        modifyWindow = SetingWindow(
            self.rootDir + self.setingName,
            self.dbPathList
        )
        modifyWindow.exec()
        # 更新历史修改记录
        if (self.setingName == self.historySeting):
            self.updataState('yes')
            # 操作数据库
            self.txtDb.path = self.historySavPath
            dbStateCheck(
                self,
                self.txtDb.modifyIndexData,
                None,
                [{2: 'yes'}]
            )

    # 新建配置
    @errMsgBox
    def _newSeting(self, event):
        if (not os.path.exists(self.setingSavPath)):
            self.errMsg = self.errMsg + '\n保存配置信息文件不存在，新建配置出错'
            return
        # 打开输入框并去左右空格
        setingName, ok = QtWidgets.QInputDialog.getText(
            self,
            '新建配置',
            '\n请输入配置名：(尽量不要输入;/\等字符)\n',
        )
        setingName = setingName.lstrip(' ').rstrip(' ')
        if (not len(setingName)):
            return
        # 处理重名情况
        basePath = repeatDirPathHandle(self.rootDir + setingName)
        setingName = basePath.split('/')[-1]
        # 新建配置文件夹和文件
        os.makedirs(basePath)
        initData = [
            ['./browser/src'],
            [],
            ['.png', '.jpg', '.gif'],
            [],
            ['3', '1', '1'],
        ]
        for index, file in enumerate(self.dbPathList):
            self.txtDb.path = basePath + file
            self.txtDb.clearAll()
            self.txtDb.addDatas(initData[index])
        self.listWidget.addItem(setingName)
        self.setingSum += 1
        # 操作数据库
        self.txtDb.path = self.setingSavPath
        dbStateCheck(self, self.txtDb.addOneData, None, [setingName])
        # 更新显示
        self.listWidget.scrollToBottom()
        self.selectedRow = -1
        self.selectedLabel.setText('已选择配置：')
        self.infoBox("\n配置【{}】新建成功！\n".format(setingName))

    # 删除配置
    @errMsgBox
    def _deleteSeting(self, event):
        # 选中检查
        if (self.selectedRow == -1):
            self.infoBox("\n请选中某个配置后再操作！\n")
            return
        # 删除提醒
        if (self.questionBox("\n确认要删除选中配置？\n") == QtWidgets.QMessageBox.No):
            return
        # 路径不存在错误信息
        if (not os.path.exists(self.setingSavPath)):
            self.errMsg = self.errMsg + '\n保存配置信息文件不存在，删除配置出错'
            return
        # 要删除的配置已载入
        if (self.setingName == self.historySeting):
            self.infoBox('\n要删除的配置【{}】处于载入状态，删除失败\n'.format(self.setingName))
            return
        # 删除列表元素
        self.listWidget.takeItem(self.selectedRow)
        self.setingSum -= 1
        # 操纵数据库
        self.txtDb.path = self.setingSavPath
        dbStateCheck(self, self.txtDb.deleteIndexData, None, [[self.selectedRow + 1]])
        # 删除配置文件
        deletePath = self.rootDir + self.setingName
        if (os.path.exists(deletePath)):
            shutil.rmtree(deletePath)
        # 更新显示
        self.selectedLabel.setText('已选择配置：')
        self.selectedRow = -1
        self.infoBox("\n配置【{}】删除成功！\n".format(self.setingName))

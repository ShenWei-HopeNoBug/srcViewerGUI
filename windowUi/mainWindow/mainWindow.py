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
        self.txtDb = TxtDatabase('./config/seting.txt')  # ����txtDb����
        self.rootDir = rootDir + '/'  # ����Ŀ¼���ļ���
        self.setingName = setingName  # ������
        self.dbPathList = dbPathList  # txtDb����·�����ļ����б�
        self.setingSavPath = './config/seting.txt'  # ���������ļ�·��
        self.historySavPath = './config/history.txt'  # ������ʷ��¼�ļ�·��
        self.errMsg = ''  # ������Ϣ
        self.selectedRow = -1  # ѡ��listItem������(-1����ûѡ��)
        self.setingSum = 0  # ��������
        self.historySeting = ''  # ������ʷ��¼
        # ��ʼ��Ui
        self.initUi()
        # ���¼�
        self.listWidget.itemClicked.connect(self._itemShow)
        self.btnLoadSeting.clicked.connect(self._loadSeting)
        self.btnModifySeting.clicked.connect(self._modifySeting)
        self.btnNewSeting.clicked.connect(self._newSeting)
        self.btnDeleteSeting.clicked.connect(self._deleteSeting)
        self.btnBrowser.clicked.connect(self._openBrowser)

    # ��ʼ��Ui
    @errMsgBox
    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('��ԴԤ��v1.0      �㹤���еB406')
        # �����½������ļ�
        self.checkDefault()
        # �����б����ʷ��¼
        self.itemLoad()
        self.loadHistory()

    # ��һ�δ��½�Ĭ�������ļ�
    @errMsgBox
    def checkDefault(self):
        # �����ʷ��¼�ļ�
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
        # ��������ļ�
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

    # ------------------------------��������
    # ���������б�
    @errMsgBox
    def itemLoad(self):
        if (not os.path.exists(self.setingSavPath)):
            self.errMsg = self.errMsg + '\n���ü�¼�ļ�·�������ڣ����������б�ʧ��'
            return
        # �������ݿ�
        self.txtDb.path = self.setingSavPath
        self.listWidget.addItems(dbStateCheck(self, self.txtDb.printDatas, []))
        self.setingSum = dbStateCheck(self, self.txtDb.getDataSum, 0)

    # ������ʷ��¼��Ϣ
    @errMsgBox
    def loadHistory(self):
        if (not os.path.exists(self.historySavPath)):
            self.errMsg = self.errMsg + '\n��ʷ��¼�ļ�·�������ڣ�������ʷ��¼ʧ��'
            return
        # �������ݿ�
        self.txtDb.path = self.historySavPath
        historyList = dbStateCheck(self, self.txtDb.printDatas, ['', 'no'])
        # ������ʾ
        self.historyLabel.setText('���������ã�{}'.format(historyList[0]))
        self.historySeting = historyList[0]
        self.updataState(historyList[1])

    # ����������ʷ��ʾ
    @errMsgBox
    def updataState(self, state):
        # �ж�״̬
        if (self.historySeting == ''):
            self.stateLabel.setText('״̬��')
        elif (state == 'yes'):
            self.stateLabel.setText('״̬�����޸Ķ���')
        else:
            self.stateLabel.setText('״̬�����޸�')

    # ������ʾ��
    def infoBox(self, msg):
        QtWidgets.QMessageBox.information(
            self,
            "����",
            msg
        )

    # ����ѯ�ʿ�
    def questionBox(self, msg):
        return QtWidgets.QMessageBox.question(
            self,
            'ѯ��',
            msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

    # ��ȡ·�����ò�д��JS
    def rwPathList(self):
        basePath = self.rootDir + self.setingName
        # ��ȡ·������
        pathSetingList = []
        for file in self.dbPathList[0:4]:
            self.txtDb.path = basePath + file
            pathSetingList.append(dbStateCheck(self, self.txtDb.printDatas, []))
        # ȥ���ظ��ͱ�������·��
        pathSetingList[0] = pathDetection(pathSetingList[0])
        pathSetingList[1] = pathDetection(pathSetingList[1])
        pathSetingList[2] = list(set(pathSetingList[2]))
        pathSetingList[3] = list(set(pathSetingList[3]))
        # ��·����Ϊ����·��
        pathSetingList[0] = [os.path.abspath(path) for path in pathSetingList[0]]
        pathSetingList[1] = [os.path.abspath(path) for path in pathSetingList[1]]
        pathList = getSortPathList(*pathSetingList)
        # д��·������
        if (not pathList):
            self.infoBox('\n����Ŀ¼��ָ���ļ���\n')
            return False
        writePathTojs(pathList, "./browser/js/pathList.js")
        return True

    # ��ȡ��ʾ���ò�д��JS
    def rwShowList(self):
        self.txtDb.path = self.rootDir + self.setingName + self.dbPathList[4]
        showSetingList = dbStateCheck(self, self.txtDb.printDatas, [])
        showSetingList = [int(value) for value in showSetingList]
        # д����ʾ����
        writeShowTojs("./browser/js/options.js", *showSetingList)

    # �رմ���ȷ��
    def closeEvent(self, event):
        if (self.questionBox("ȷ���˳���") == QtWidgets.QMessageBox.Yes):
            event.accept()
        else:
            event.ignore()

    # ------------------------------���¼�
    # �������
    @errMsgBox
    def _openBrowser(self, event):
        browserPath = "./browser/html/index.html"
        if (not os.path.exists(browserPath)):
            self.infoBox('\nԤ��html�ļ������ڣ�\n')
        if (self.questionBox('\n�Ƿ���������\n') == QtWidgets.QMessageBox.Yes):
            webbrowser.open(os.path.abspath(browserPath))

    # ��ʾѡ����
    @errMsgBox
    def _itemShow(self, item):
        self.selectedLabel.setText('��ѡ�����ã�{}'.format(item.text()))
        # ����ѡ������������
        self.selectedRow = self.listWidget.selectedIndexes()[0].row()
        self.setingName = self.listWidget.item(self.selectedRow).text()

    # ����ѡ������
    @errMsgBox
    def _loadSeting(self, event):
        # �Ƿ�ѡ������
        if (self.selectedRow == -1):
            self.infoBox("\n��ѡ��ĳ�����ú��ٲ�����\n")
            return
        # ���ѡ�������Ƿ���������
        if (not fileAllExists(self.rootDir + self.setingName, self.dbPathList)['state']):
            self.infoBox("\n���á�{}���ļ���������\n".format(self.setingName))
            return
        # -----------------------corn start------------------------
        if (not (self.setingName == self.historySeting)):
            if (not self.rwPathList()):
                return
            self.rwShowList()
        else:
            if (self.questionBox('\n�Ƿ�����·������\n') == QtWidgets.QMessageBox.Yes):
                if (not self.rwPathList()):
                    return
                self.infoBox('\n�������á�{}����·�����óɹ�\n'.format(self.setingName))
            time.sleep(0.1)
            if (self.questionBox('\n�Ƿ�������ʾ����\n') == QtWidgets.QMessageBox.Yes):
                self.rwShowList()
                self.infoBox('\n�������á�{}������ʾ���óɹ�\n'.format(self.setingName))
            self.txtDb.path = self.historySavPath
            # �����޸�״̬
            dbStateCheck(
                self,
                self.txtDb.modifyIndexData,
                None,
                [{2: 'no'}]
            )
            self.updataState('no')
            return
        # -----------------------corn end------------------------
        # �������ݿ��޸���ʷ��¼
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
        # ������ʾ
        self.historySeting = data
        self.historyLabel.setText('���������ã�{}'.format(self.setingName))
        self.updataState('no')
        self.infoBox('\n�������á�{}����·������ʾ���óɹ�\n'.format(self.setingName))

    # �޸�ѡ������
    @errMsgBox
    def _modifySeting(self, event):
        if (self.selectedRow == -1):
            self.infoBox("\n��ѡ��ĳ�����ú��ٲ�����\n")
            return
        # �����ô���
        modifyWindow = SetingWindow(
            self.rootDir + self.setingName,
            self.dbPathList
        )
        modifyWindow.exec()
        # ������ʷ�޸ļ�¼
        if (self.setingName == self.historySeting):
            self.updataState('yes')
            # �������ݿ�
            self.txtDb.path = self.historySavPath
            dbStateCheck(
                self,
                self.txtDb.modifyIndexData,
                None,
                [{2: 'yes'}]
            )

    # �½�����
    @errMsgBox
    def _newSeting(self, event):
        if (not os.path.exists(self.setingSavPath)):
            self.errMsg = self.errMsg + '\n����������Ϣ�ļ������ڣ��½����ó���'
            return
        # �������ȥ���ҿո�
        setingName, ok = QtWidgets.QInputDialog.getText(
            self,
            '�½�����',
            '\n��������������(������Ҫ����;/\���ַ�)\n',
        )
        setingName = setingName.lstrip(' ').rstrip(' ')
        if (not len(setingName)):
            return
        # �����������
        basePath = repeatDirPathHandle(self.rootDir + setingName)
        setingName = basePath.split('/')[-1]
        # �½������ļ��к��ļ�
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
        # �������ݿ�
        self.txtDb.path = self.setingSavPath
        dbStateCheck(self, self.txtDb.addOneData, None, [setingName])
        # ������ʾ
        self.listWidget.scrollToBottom()
        self.selectedRow = -1
        self.selectedLabel.setText('��ѡ�����ã�')
        self.infoBox("\n���á�{}���½��ɹ���\n".format(setingName))

    # ɾ������
    @errMsgBox
    def _deleteSeting(self, event):
        # ѡ�м��
        if (self.selectedRow == -1):
            self.infoBox("\n��ѡ��ĳ�����ú��ٲ�����\n")
            return
        # ɾ������
        if (self.questionBox("\nȷ��Ҫɾ��ѡ�����ã�\n") == QtWidgets.QMessageBox.No):
            return
        # ·�������ڴ�����Ϣ
        if (not os.path.exists(self.setingSavPath)):
            self.errMsg = self.errMsg + '\n����������Ϣ�ļ������ڣ�ɾ�����ó���'
            return
        # Ҫɾ��������������
        if (self.setingName == self.historySeting):
            self.infoBox('\nҪɾ�������á�{}����������״̬��ɾ��ʧ��\n'.format(self.setingName))
            return
        # ɾ���б�Ԫ��
        self.listWidget.takeItem(self.selectedRow)
        self.setingSum -= 1
        # �������ݿ�
        self.txtDb.path = self.setingSavPath
        dbStateCheck(self, self.txtDb.deleteIndexData, None, [[self.selectedRow + 1]])
        # ɾ�������ļ�
        deletePath = self.rootDir + self.setingName
        if (os.path.exists(deletePath)):
            shutil.rmtree(deletePath)
        # ������ʾ
        self.selectedLabel.setText('��ѡ�����ã�')
        self.selectedRow = -1
        self.infoBox("\n���á�{}��ɾ���ɹ���\n".format(self.setingName))

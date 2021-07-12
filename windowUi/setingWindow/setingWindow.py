# -*- coding: GB2312 -*-
from PyQt5 import QtWidgets
from .setingWindow_ui import Ui_setingWindow
from windowUi.dataManager.dataManager import DataManager
from assets.publicTools import errMsgBox, dbStateCheck
from assets.txtDataBase import TxtDatabase

'''
self.dbPathList Ĭ��ֵ��
[
    '/DirList.txt',
    '/DirIgnore.txt',
    '/ExtList.txt',
    '/ExtIgnore.txt',
    '/OtherSeting.txt',
]
'''


# ************************************���ô���
class SetingWindow(QtWidgets.QDialog, Ui_setingWindow):
    def __init__(self, dbBaseDir, dbPathList):
        super(SetingWindow, self).__init__()
        self.txtDb = TxtDatabase(dbBaseDir + dbPathList[0])  # ����txtDb����
        self.dbBaseDir = dbBaseDir  # txtDb����·����Ŀ¼
        self.dbPathList = dbPathList  # txtDb����·�����ļ����б�
        self.otherSeting = []  # otherSeting��������
        self.errMsg = ''  # ������Ϣ
        self.rbtnGroup = QtWidgets.QButtonGroup(self)  # ��ѡ��ť����
        self.btnGroup = QtWidgets.QButtonGroup(self)  # �����ť����
        # ��ʼ��UI
        self.initUi()
        # ���õ�ѡ��ť����
        self.rbtnGroup.addButton(self.rbtnImage, id=1)
        self.rbtnGroup.addButton(self.rbtnVideo, id=2)
        # ���õ����ť����
        self.btnGroup.addButton(self.btnDirList, id=0)
        self.btnGroup.addButton(self.btnDirIgnore, id=1)
        self.btnGroup.addButton(self.btnExtList, id=2)
        self.btnGroup.addButton(self.btnExtIgnore, id=3)
        # ���¼�
        self.spinBoxMaxRow.valueChanged.connect(self._maxRowChanged)
        self.spinBoxStartPage.valueChanged.connect(self._startPageChanged)
        self.rbtnGroup.buttonClicked.connect(self._modelChanged)
        self.btnGroup.buttonClicked.connect(self._setingModify)
        self.btnBoxConfirm.clicked.connect(self._savOtherSeting)

    # ��ʼ��UI
    @errMsgBox
    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('�޸�����')
        self.titleLabel.setText('�����ļ�����{}'.format(self.dbBaseDir.split('/')[-1]))
        # ���Ƽ���������
        self.spinBoxMaxRow.setMinimum(1)
        self.spinBoxStartPage.setMinimum(1)
        # ��������
        self.loadSeting()

    # ------------------------------��������
    # ���ر����otherSeting����
    @errMsgBox
    def loadSeting(self):
        # �������ݿ�
        self.txtDb.path = self.dbBaseDir + self.dbPathList[4]  # �޸�dbtxt·��
        self.otherSeting = dbStateCheck(self, self.txtDb.printDatas, ['3', '1', '1'])
        # ���ü�����
        self.spinBoxMaxRow.setValue(int(self.otherSeting[0]))
        self.spinBoxStartPage.setValue(int(self.otherSeting[1]))
        # ���õ�ѡ��ť
        if (self.otherSeting[2] == '1'):
            self.rbtnImage.click()
        else:
            self.rbtnVideo.click()

    # ���޸������Ӵ���
    @errMsgBox
    def openModifyWindow(self, dataName, dbPathIndex):
        dbWorkPath = self.dbBaseDir + self.dbPathList[dbPathIndex]
        modifyWindow = DataManager(dataName, dbWorkPath)
        modifyWindow.exec()

    # ------------------------------���¼�
    # �����޸ĵ�otherSeting���ò��˳�
    @errMsgBox
    def _savOtherSeting(self, btn):
        if (btn.text() == 'OK'):
            # �������ݿ�
            modifyDict = {index + 1: value for index, value in enumerate(self.otherSeting)}
            self.txtDb.path = self.dbBaseDir + self.dbPathList[4]  # �޸�dbtxt·��
            dbStateCheck(self, self.txtDb.modifyIndexData, None, [modifyDict])
        self.close()

    # ��ҳ�����仯
    @errMsgBox
    def _maxRowChanged(self, value):
        self.otherSeting[0] = str(value)

    # ��������仯
    @errMsgBox
    def _startPageChanged(self, value):
        self.otherSeting[1] = str(value)

    # ģʽ�仯
    @errMsgBox
    def _modelChanged(self, rbtn):
        # �洢��ťid��
        self.otherSeting[2] = str(self.rbtnGroup.id(rbtn))

    # ���ݰ�ťid�򿪶�Ӧ�޸Ĵ���
    @errMsgBox
    def _setingModify(self, btn):
        self.openModifyWindow(btn.text(), self.btnGroup.id(btn))

# -*- coding: GB2312 -*-
from PyQt5 import QtWidgets, QtGui
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
        self.rbtnGroup.addButton(self.rbtnMusic, id=3)
        # ���õ����ť����
        self.btnGroup.addButton(self.btnDirList, id=0)
        self.btnGroup.addButton(self.btnDirIgnore, id=1)
        self.btnGroup.addButton(self.btnExtList, id=2)
        self.btnGroup.addButton(self.btnExtIgnore, id=3)
        # ���¼�
        self.spinBoxMaxRow.valueChanged.connect(self._maxRowChanged)
        self.spinBoxStartPage.valueChanged.connect(self._startPageChanged)
        self.spinBoxSizeMin.valueChanged.connect(self._sizeMinChanged)
        self.spinBoxSizeMax.valueChanged.connect(self._sizeMaxChanged)
        self.checkBoxPlace.stateChanged.connect(self._placeChanged)
        self.rbtnGroup.buttonClicked.connect(self._modelChanged)
        self.btnGroup.buttonClicked.connect(self._setingModify)

    # ��ʼ��UI
    @errMsgBox
    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('�޸�����')
        self.titleLabel.setText('�����ļ�����{}'.format(self.dbBaseDir.split('/')[-1]))
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setFixedSize(self.width(), self.height())
        # ����������ʽ
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
        # ���Ƽ�����������
        self.spinBoxMaxRow.setMinimum(1)
        self.spinBoxMaxRow.setMaximum(12)
        self.spinBoxStartPage.setMinimum(1)
        self.spinBoxStartPage.setMaximum(9999999)
        self.spinBoxSizeMin.setMinimum(0)
        self.spinBoxSizeMin.setMaximum(10240)
        self.spinBoxSizeMax.setMinimum(1)
        self.spinBoxSizeMax.setMaximum(20480)
        # ��������
        self.loadSeting()

    # ------------------------------��������
    # ���ر����otherSeting����
    @errMsgBox
    def loadSeting(self):
        # �������ݿ�
        self.txtDb.path = self.dbBaseDir + self.dbPathList[4]  # �޸�dbtxt·��
        self.otherSeting = dbStateCheck(self, self.txtDb.printDatas, ['3', '1', '/image', '0', '10', '0'])
        # ���ü�����
        self.spinBoxMaxRow.setValue(int(self.otherSeting[0]))
        self.spinBoxStartPage.setValue(int(self.otherSeting[1]))
        self.spinBoxSizeMin.setValue(int(self.otherSeting[3]))
        self.spinBoxSizeMax.setValue(int(self.otherSeting[4]))
        # ���õ�ѡ��ť
        if (self.otherSeting[2] == '/image'):
            self.rbtnImage.click()
        elif (self.otherSeting[2] == '/video'):
            self.rbtnVideo.click()
        elif (self.otherSeting[2] == '/music'):
            self.rbtnMusic.click()
        # ���ù�ѡ��
        if (int(self.otherSeting[5])):
            self.checkBoxPlace.click()

    # ���޸������Ӵ���
    @errMsgBox
    def openModifyWindow(self, dataName, dbPathIndex):
        dbWorkPath = self.dbBaseDir + self.dbPathList[dbPathIndex]
        modifyWindow = DataManager(dataName, dbWorkPath)
        modifyWindow.exec()

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

    # �����޸ĵ�otherSeting����
    @errMsgBox
    def savOtherSeting(self):
        modifyDict = {index + 1: value for index, value in enumerate(self.otherSeting)}
        # �������ݿ�
        self.txtDb.path = self.dbBaseDir + self.dbPathList[4]  # �޸�dbtxt·��
        dbStateCheck(self, self.txtDb.modifyIndexData, None, [modifyDict])

    # �رմ���ȷ�ϲ������޸�����
    def closeEvent(self, event):
        if (self.questionBox("�޸�������ɣ�") == QtWidgets.QMessageBox.Yes):
            self.savOtherSeting()
            event.accept()
        else:
            event.ignore()

    # ------------------------------���¼�
    # ��ҳ�����仯
    @errMsgBox
    def _maxRowChanged(self, value):
        self.otherSeting[0] = str(value)

    # ��ʼҳ��仯
    @errMsgBox
    def _startPageChanged(self, value):
        self.otherSeting[1] = str(value)

    # ģʽ�仯
    @errMsgBox
    def _modelChanged(self, rbtn):
        # �洢��ťid��
        id = self.rbtnGroup.id(rbtn)
        if (id == 1):
            self.otherSeting[2] = '/image'
        elif (id == 2):
            self.otherSeting[2] = '/video'
        else:
            self.otherSeting[2] = '/music'

    # �ļ���С���ޱ仯
    @errMsgBox
    def _sizeMinChanged(self, value):
        maxSize = self.spinBoxSizeMax.value()
        if (value >= maxSize):
            self.spinBoxSizeMax.setValue(value + 1)
        self.otherSeting[3] = str(value)

    @errMsgBox
    # �ļ���С���ޱ仯
    def _sizeMaxChanged(self, value):
        minSize = self.spinBoxSizeMin.value()
        if (value <= minSize):
            self.spinBoxSizeMin.setValue(value - 1)
        self.otherSeting[4] = str(value)

    # ��ѡ�򱻵��
    @errMsgBox
    def _placeChanged(self, state):
        if (state == 2):
            state = 1
        self.otherSeting[5] = str(state)

    # ���ݰ�ťid�򿪶�Ӧ�޸Ĵ���
    @errMsgBox
    def _setingModify(self, btn):
        self.openModifyWindow(btn.text(), self.btnGroup.id(btn))

# -*- coding: GB2312 -*-
import re
from PyQt5 import QtWidgets
from .dataManager_ui import Ui_dataManager
from windowUi.dataInput.dataInput import DataInput
from assets.publicTools import errMsgBox, dbStateCheck
from assets.txtDataBase import TxtDatabase


# ********************************���ݹ���UI
class DataManager(QtWidgets.QDialog, Ui_dataManager):
    def __init__(self, dataName, dbWorkPath):
        super(DataManager, self).__init__()
        # ʵ��˽�б���
        self.dataName = dataName  # ����������
        self.txtDb = TxtDatabase(dbWorkPath)  # ���ӵ�txt���ݿ�
        self.dataSum = 0  # ��������
        self.selectedRow = -1  # ѡ��listItem������(-1����ûѡ��)
        self.errMsg = ''  # �쳣����
        self.signData = ''  # ���Ӵ��ڽ��յ�������
        # ��ʼ��Ui
        self.initUi()
        # ���¼�
        self.listWidget.itemClicked.connect(self._itemShow)
        self.btnAddData.clicked.connect(self._itemAdd)
        self.btnModifyData.clicked.connect(self._itemModify)
        self.btnDeleteData.clicked.connect(self._itemDelete)
        self.btnClearAll.clicked.connect(self._itemClearAll)

    # ----------------------��������
    # ��ʼ��UI
    @errMsgBox
    def initUi(self):
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.dataNameLabel.setText("��������{}".format(self.dataName))
        self.setWindowTitle("��{}�����ݹ���".format(self.dataName))
        # ���ݿ��������
        self.itemLoad()

    # ���մ��Ӵ��ڴ���������
    @errMsgBox
    def getSignData(self, signData):
        self.signData = signData

    # ----------------------��ʾ
    # ��������������ʾ
    @errMsgBox
    def updataDataSumLabel(self):
        self.dataSumLabel.setText("��������{}".format(self.dataSum))

    # ----------------------�������
    # �����ݿ�����б�����
    @errMsgBox
    def itemLoad(self):
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n���ݿ�·�������ڣ��������ݳ���'
            return
        # �������ݿ�
        self.listWidget.addItems(dbStateCheck(self, self.txtDb.printDatas, []))
        self.dataSum = dbStateCheck(self, self.txtDb.getDataSum, 0)
        self.updataDataSumLabel()

    # ----------------------���¼�
    # ��ʾѡ����
    @errMsgBox
    def _itemShow(self, item):
        self.dataDetail.clear()
        self.selectedRow = self.listWidget.selectedIndexes()[0].row()
        self.dataDetail.append('���� {} ��'.format(self.selectedRow + 1))
        self.dataDetail.append(item.text())
        # �������ö�
        self.dataDetail.verticalScrollBar().setValue(0)

    # ����б�����
    @errMsgBox
    def _itemClearAll(self, event):
        if (self.dataSum == 0):
            return
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n���ݿ�·�������ڣ�������ݳ���'
            return
        # ȷ�ϵ���
        reply = QtWidgets.QMessageBox.question(
            self,
            '����',
            "\n��պ��޷��ָ���ȷ��Ҫɾ��ȫ�����ݣ�\n",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if (reply == QtWidgets.QMessageBox.No):
            return
        # ��ʼɾ��
        self.listWidget.clear()
        # �������ݿ�
        dbStateCheck(self, self.txtDb.clearAll)
        # ������ʾ
        self.dataDetail.clear()
        self.dataSum = 0
        self.updataDataSumLabel()
        QtWidgets.QMessageBox.information(
            self,
            "����",
            "\n������ȫ��ɾ����\n"
        )

    # ɾ��ѡ����
    @errMsgBox
    def _itemDelete(self, event):
        if (self.selectedRow == -1):
            QtWidgets.QMessageBox.information(
                self,
                "����",
                "\n��ѡ��һ�����ݺ��ٲ�����\n"
            )
            return
        # ɾ������
        reply = QtWidgets.QMessageBox.question(
            self,
            '����',
            "\nȷ��Ҫɾ��ѡ�����ݣ�\n",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if (reply == QtWidgets.QMessageBox.No):
            return
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n���ݿ�·�������ڣ�ɾ�����ݳ���'
            return
        # ��ʼɾ��
        self.listWidget.takeItem(self.selectedRow)
        # �������ݿ�
        dbStateCheck(self, self.txtDb.deleteIndexData, None, [[self.selectedRow + 1]])
        self.selectedRow = -1
        # ������ʾ
        self.dataSum -= 1
        self.updataDataSumLabel()
        self.dataDetail.clear()

    # �޸�ѡ����
    @errMsgBox
    def _itemModify(self, event):
        if (self.selectedRow == -1):
            QtWidgets.QMessageBox.information(
                self,
                "����",
                "\n��ѡ��һ�����ݺ��ٲ�����\n"
            )
            return
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n���ݿ�·�������ڣ��޸����ݳ���'
            return
        self.signData = ''
        oldData = self.listWidget.item(self.selectedRow).text()
        # �������Ӵ���
        modifyWindow = DataInput(
            self.dataName,
            '��{}�������޸�'.format(self.dataName),
            '���޸�����(���Ƽ�Enter���С�Tab�����Ȳ���)',
            oldData
        )
        modifyWindow._signal.connect(self.getSignData)
        modifyWindow.exec()
        # û���������ݲ��޸�
        newData = self.signData.lstrip('\n').rstrip('\n')
        self.signData = ''
        if (newData == '' or newData == oldData):
            return

        # �޸��б�����
        self.listWidget.takeItem(self.selectedRow)
        self.listWidget.insertItem(self.selectedRow, newData)
        self.listWidget.setCurrentRow(self.selectedRow)
        # �������ݿ�
        dbStateCheck(self,
                     self.txtDb.modifyIndexData,
                     None,
                     [{self.selectedRow + 1: newData}]
                     )
        # ������ʾ
        self.dataDetail.clear()
        self.dataDetail.append(newData)

        # ������ʾ����ʾ����(���뻻�з�)
        def strLimit(string, limit):
            countLine = len(string) // limit
            string = list(string)
            for index in range(countLine):
                string.insert(limit * (index + 1) + index, '\n')
            return ''.join(string)

        limit = 40  # ���������ַ���
        oldData = strLimit(oldData, limit)
        newData = strLimit(newData, limit)
        QtWidgets.QMessageBox.information(
            self,
            "����",
            "\n�����޸ĳɹ���\nԭ���ݣ�{}\n=>\n�����ݣ�{}".format(oldData, newData)
        )

    # ���������
    @errMsgBox
    def _itemAdd(self, event):
        if (not self.txtDb.pathCheck()):
            self.errMsg = self.errMsg + '\n���ݿ�·�������ڣ�������ݳ���'
            return
        self.signData = ''
        # �������Ӵ���
        inputWindow = DataInput(self.dataName)
        inputWindow._signal.connect(self.getSignData)
        inputWindow.exec()
        # û���������ݲ��޸�
        if (self.signData == ''):
            return
        # �������ݲ�ȥ�س���
        data = self.signData.lstrip('\n').rstrip('\n')
        data = re.sub(r'\n+', '\n', data)
        data = data.split('\n')
        # �������
        self.listWidget.addItems(data)
        self.dataSum += len(data)
        # �������ݿ�
        dbStateCheck(self, self.txtDb.addDatas, None, [data])
        # ������ʾ
        self.listWidget.scrollToBottom()
        self.dataDetail.clear()
        self.selectedRow = -1
        self.updataDataSumLabel()
        self.signData = ''

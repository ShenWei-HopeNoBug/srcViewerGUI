# -*- coding: GB2312 -*-
from PyQt5 import QtWidgets, QtCore
from .dataInput_ui import Ui_DataInput


# ********************************�ı�����UI
class DataInput(QtWidgets.QDialog, Ui_DataInput):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, dataName, winTitle='', title='', initTxt=''):
        super().__init__()
        self.dataName = dataName
        self.winTitle = winTitle
        self.title = title
        self.initTxt = initTxt
        # ��ʼ��UI
        self.initUi()
        # �󶨰�ť�¼�
        self.btnBoxConfirm.clicked.connect(self._signalSend)
        self.btnAddPath.clicked.connect(self._addBrowerPath)

    # ��ʼ��UI
    def initUi(self):
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        if (not self.winTitle == ''):
            self.setWindowTitle(self.winTitle)
        else:
            self.setWindowTitle("��{}����������".format(self.dataName))
        if (not self.title == ''):
            self.titleLabel.setText(self.title)
        if (not self.initTxt == ''):
            self.textEdit.append(self.initTxt)
            self.textEdit.verticalScrollBar().setValue(0)

    # ----------------------���¼�
    # ������·��
    def _addBrowerPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "���")
        self.textEdit.append(path)

    # �����ź�
    def _signalSend(self, btn):
        if (btn.text() == 'OK'):
            self._signal.emit(self.textEdit.toPlainText())

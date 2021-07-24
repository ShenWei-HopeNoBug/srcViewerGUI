# -*- coding: GB2312 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from .dataInput_ui import Ui_dataInput


# ********************************�ı�����UI
class DataInput(QtWidgets.QDialog, Ui_dataInput):
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
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
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
            # ����������ʽ
            self.setWindowOpacity(0.95)
        winStyle = '''
        #dataInput{
            background-color:rgb(255, 224, 178);
        }
        
        QTextEdit{
            background-color:rgb(251,232,204);
        }
        '''
        self.setStyleSheet(winStyle)

    # ----------------------���¼�
    # ������·��
    def _addBrowerPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "���")
        self.textEdit.append(path)

    # �����ź�
    def _signalSend(self, btn):
        if (btn.text() == 'OK'):
            self._signal.emit(self.textEdit.toPlainText())

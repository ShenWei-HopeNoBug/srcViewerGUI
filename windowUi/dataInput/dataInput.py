# -*- coding: GB2312 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from .dataInput_ui import Ui_dataInput


# ********************************文本输入UI
class DataInput(QtWidgets.QDialog, Ui_dataInput):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, dataName, winTitle='', title='', initTxt=''):
        super().__init__()
        self.dataName = dataName
        self.winTitle = winTitle
        self.title = title
        self.initTxt = initTxt
        # 初始化UI
        self.initUi()
        # 绑定按钮事件
        self.btnBoxConfirm.clicked.connect(self._signalSend)
        self.btnAddPath.clicked.connect(self._addBrowerPath)

    # 初始化UI
    def initUi(self):
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setFixedSize(self.width(), self.height())
        if (not self.winTitle == ''):
            self.setWindowTitle(self.winTitle)
        else:
            self.setWindowTitle("【{}】数据输入".format(self.dataName))
        if (not self.title == ''):
            self.titleLabel.setText(self.title)
        if (not self.initTxt == ''):
            self.textEdit.append(self.initTxt)
            self.textEdit.verticalScrollBar().setValue(0)
            # 设置美化样式
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

    # ----------------------绑定事件
    # 添加浏览路径
    def _addBrowerPath(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "浏览")
        self.textEdit.append(path)

    # 发送信号
    def _signalSend(self, btn):
        if (btn.text() == 'OK'):
            self._signal.emit(self.textEdit.toPlainText())

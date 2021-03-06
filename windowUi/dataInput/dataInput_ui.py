# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dataInput.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dataInput(object):
    def setupUi(self, dataInput):
        dataInput.setObjectName("dataInput")
        dataInput.resize(640, 480)
        self.titleLabel = QtWidgets.QLabel(dataInput)
        self.titleLabel.setGeometry(QtCore.QRect(20, 10, 561, 61))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.btnAddPath = QtWidgets.QPushButton(dataInput)
        self.btnAddPath.setGeometry(QtCore.QRect(486, 78, 104, 32))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.btnAddPath.setFont(font)
        self.btnAddPath.setObjectName("btnAddPath")
        self.verticalLayoutWidget = QtWidgets.QWidget(dataInput)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 130, 541, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.btnBoxConfirm = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.btnBoxConfirm.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnBoxConfirm.setFont(font)
        self.btnBoxConfirm.setOrientation(QtCore.Qt.Horizontal)
        self.btnBoxConfirm.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnBoxConfirm.setObjectName("btnBoxConfirm")
        self.verticalLayout.addWidget(self.btnBoxConfirm)

        self.retranslateUi(dataInput)
        self.btnBoxConfirm.accepted.connect(dataInput.accept)
        self.btnBoxConfirm.rejected.connect(dataInput.reject)
        QtCore.QMetaObject.connectSlotsByName(dataInput)

    def retranslateUi(self, dataInput):
        _translate = QtCore.QCoreApplication.translate
        dataInput.setWindowTitle(_translate("dataInput", "Dialog"))
        self.titleLabel.setText(_translate("dataInput", "请输入数据(输入多个数据请用Enter换行隔开)"))
        self.btnAddPath.setText(_translate("dataInput", "添加路径"))

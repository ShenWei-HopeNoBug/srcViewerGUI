# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(640, 480)
        self.selectedLabel = QtWidgets.QLabel(mainWindow)
        self.selectedLabel.setGeometry(QtCore.QRect(30, 148, 590, 44))
        self.selectedLabel.setMinimumSize(QtCore.QSize(0, 44))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.selectedLabel.setFont(font)
        self.selectedLabel.setObjectName("selectedLabel")
        self.historyLabel = QtWidgets.QLabel(mainWindow)
        self.historyLabel.setGeometry(QtCore.QRect(30, 20, 590, 44))
        self.historyLabel.setMinimumSize(QtCore.QSize(0, 44))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.historyLabel.setFont(font)
        self.historyLabel.setObjectName("historyLabel")
        self.horizontalLayoutWidget = QtWidgets.QWidget(mainWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 60, 531, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stateLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.stateLabel.setMinimumSize(QtCore.QSize(243, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.stateLabel.setFont(font)
        self.stateLabel.setObjectName("stateLabel")
        self.horizontalLayout.addWidget(self.stateLabel)
        self.btnLoadSeting = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnLoadSeting.setMinimumSize(QtCore.QSize(123, 52))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.btnLoadSeting.setFont(font)
        self.btnLoadSeting.setObjectName("btnLoadSeting")
        self.horizontalLayout.addWidget(self.btnLoadSeting)
        self.btnBrowser = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnBrowser.setMinimumSize(QtCore.QSize(123, 52))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.btnBrowser.setFont(font)
        self.btnBrowser.setObjectName("btnBrowser")
        self.horizontalLayout.addWidget(self.btnBrowser)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(mainWindow)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(59, 210, 531, 221))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(40)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnNewSeting = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.btnNewSeting.setMinimumSize(QtCore.QSize(0, 44))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.btnNewSeting.setFont(font)
        self.btnNewSeting.setObjectName("btnNewSeting")
        self.verticalLayout.addWidget(self.btnNewSeting)
        self.btnModifySeting = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.btnModifySeting.setMinimumSize(QtCore.QSize(0, 44))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.btnModifySeting.setFont(font)
        self.btnModifySeting.setObjectName("btnModifySeting")
        self.verticalLayout.addWidget(self.btnModifySeting)
        self.btnDeleteSeting = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.btnDeleteSeting.setMinimumSize(QtCore.QSize(0, 44))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.btnDeleteSeting.setFont(font)
        self.btnDeleteSeting.setObjectName("btnDeleteSeting")
        self.verticalLayout.addWidget(self.btnDeleteSeting)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Dialog"))
        self.selectedLabel.setText(_translate("mainWindow", "已选择配置："))
        self.historyLabel.setText(_translate("mainWindow", "已载入配置："))
        self.stateLabel.setText(_translate("mainWindow", "状态："))
        self.btnLoadSeting.setText(_translate("mainWindow", "载入配置"))
        self.btnBrowser.setText(_translate("mainWindow", "打开浏览器"))
        self.label.setText(_translate("mainWindow", "配\n"
"\n"
"置\n"
"\n"
"列\n"
"\n"
"表"))
        self.btnNewSeting.setText(_translate("mainWindow", "新建配置"))
        self.btnModifySeting.setText(_translate("mainWindow", "修改配置"))
        self.btnDeleteSeting.setText(_translate("mainWindow", "删除配置"))

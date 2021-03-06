# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_setingWindow(object):
    def setupUi(self, setingWindow):
        setingWindow.setObjectName("setingWindow")
        setingWindow.resize(640, 486)
        font = QtGui.QFont()
        font.setFamily("宋体")
        setingWindow.setFont(font)
        self.titleLabel = QtWidgets.QLabel(setingWindow)
        self.titleLabel.setGeometry(QtCore.QRect(30, 20, 580, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayoutWidget = QtWidgets.QWidget(setingWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 80, 151, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnDirList = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnDirList.setMinimumSize(QtCore.QSize(0, 50))
        self.btnDirList.setObjectName("btnDirList")
        self.verticalLayout.addWidget(self.btnDirList)
        self.btnDirIgnore = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnDirIgnore.setMinimumSize(QtCore.QSize(0, 50))
        self.btnDirIgnore.setObjectName("btnDirIgnore")
        self.verticalLayout.addWidget(self.btnDirIgnore)
        self.btnExtList = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnExtList.setMinimumSize(QtCore.QSize(0, 50))
        self.btnExtList.setObjectName("btnExtList")
        self.verticalLayout.addWidget(self.btnExtList)
        self.btnExtIgnore = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnExtIgnore.setMinimumSize(QtCore.QSize(0, 50))
        self.btnExtIgnore.setObjectName("btnExtIgnore")
        self.verticalLayout.addWidget(self.btnExtIgnore)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(setingWindow)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(450, 160, 141, 181))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.spinBoxMaxRow = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBoxMaxRow.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.spinBoxMaxRow.setFont(font)
        self.spinBoxMaxRow.setMinimum(1)
        self.spinBoxMaxRow.setMaximum(12)
        self.spinBoxMaxRow.setDisplayIntegerBase(10)
        self.spinBoxMaxRow.setObjectName("spinBoxMaxRow")
        self.verticalLayout_2.addWidget(self.spinBoxMaxRow)
        self.spinBoxStartPage = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBoxStartPage.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxStartPage.setFont(font)
        self.spinBoxStartPage.setMinimum(1)
        self.spinBoxStartPage.setMaximum(9999)
        self.spinBoxStartPage.setDisplayIntegerBase(10)
        self.spinBoxStartPage.setObjectName("spinBoxStartPage")
        self.verticalLayout_2.addWidget(self.spinBoxStartPage)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(setingWindow)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(300, 170, 112, 151))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_2.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_3.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(setingWindow)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(450, 330, 151, 138))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.rbtnImage = QtWidgets.QRadioButton(self.verticalLayoutWidget_4)
        self.rbtnImage.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.rbtnImage.setFont(font)
        self.rbtnImage.setObjectName("rbtnImage")
        self.verticalLayout_4.addWidget(self.rbtnImage)
        self.rbtnVideo = QtWidgets.QRadioButton(self.verticalLayoutWidget_4)
        self.rbtnVideo.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.rbtnVideo.setFont(font)
        self.rbtnVideo.setObjectName("rbtnVideo")
        self.verticalLayout_4.addWidget(self.rbtnVideo)
        self.rbtnMusic = QtWidgets.QRadioButton(self.verticalLayoutWidget_4)
        self.rbtnMusic.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.rbtnMusic.setFont(font)
        self.rbtnMusic.setObjectName("rbtnMusic")
        self.verticalLayout_4.addWidget(self.rbtnMusic)
        self.horizontalLayoutWidget = QtWidgets.QWidget(setingWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(360, 70, 231, 91))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBoxSizeMin = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBoxSizeMin.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBoxSizeMin.setFont(font)
        self.spinBoxSizeMin.setObjectName("spinBoxSizeMin")
        self.horizontalLayout.addWidget(self.spinBoxSizeMin)
        self.spinBoxSizeMax = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBoxSizeMax.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBoxSizeMax.setFont(font)
        self.spinBoxSizeMax.setObjectName("spinBoxSizeMax")
        self.horizontalLayout.addWidget(self.spinBoxSizeMax)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(setingWindow)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(300, 350, 112, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label = QtWidgets.QLabel(setingWindow)
        self.label.setGeometry(QtCore.QRect(260, 70, 91, 89))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(setingWindow)
        self.label_5.setEnabled(True)
        self.label_5.setGeometry(QtCore.QRect(467, 50, 21, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.checkBoxPlace = QtWidgets.QCheckBox(setingWindow)
        self.checkBoxPlace.setGeometry(QtCore.QRect(60, 410, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBoxPlace.setFont(font)
        self.checkBoxPlace.setObjectName("checkBoxPlace")
        self.label_6 = QtWidgets.QLabel(setingWindow)
        self.label_6.setGeometry(QtCore.QRect(374, 132, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(setingWindow)
        QtCore.QMetaObject.connectSlotsByName(setingWindow)

    def retranslateUi(self, setingWindow):
        _translate = QtCore.QCoreApplication.translate
        setingWindow.setWindowTitle(_translate("setingWindow", "Dialog"))
        self.titleLabel.setText(_translate("setingWindow", "配置文件名：XXX"))
        self.btnDirList.setText(_translate("setingWindow", "搜索文件夹"))
        self.btnDirIgnore.setText(_translate("setingWindow", "忽略文件夹"))
        self.btnExtList.setText(_translate("setingWindow", "筛选扩展名"))
        self.btnExtIgnore.setText(_translate("setingWindow", "忽略扩展名"))
        self.label_2.setText(_translate("setingWindow", "单页行数："))
        self.label_3.setText(_translate("setingWindow", "起始页号："))
        self.rbtnImage.setText(_translate("setingWindow", "图片模式"))
        self.rbtnVideo.setText(_translate("setingWindow", "视频模式"))
        self.rbtnMusic.setText(_translate("setingWindow", "音乐模式"))
        self.label_4.setText(_translate("setingWindow", "预览模式："))
        self.label.setText(_translate("setingWindow", "大小(MB)："))
        self.label_5.setText(_translate("setingWindow", "到"))
        self.checkBoxPlace.setText(_translate("setingWindow", "超出大小范围占位"))
        self.label_6.setText(_translate("setingWindow", "0-12040        1-20480"))

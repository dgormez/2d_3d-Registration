# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Apr 10 14:03:56 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1171, 703)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gridLayout_Main = QtGui.QGridLayout()
        self.gridLayout_Main.setObjectName(_fromUtf8("gridLayout_Main"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(-1, -1, 1151, 581))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_MainTab1 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_MainTab1.setMargin(0)
        self.gridLayout_MainTab1.setObjectName(_fromUtf8("gridLayout_MainTab1"))
        self.horizontalLayout_IMGs = QtGui.QHBoxLayout()
        self.horizontalLayout_IMGs.setObjectName(_fromUtf8("horizontalLayout_IMGs"))
        self.gridLayout_MainTab1.addLayout(self.horizontalLayout_IMGs, 0, 0, 1, 1)
        self.horizontalLayout_Buttons = QtGui.QHBoxLayout()
        self.horizontalLayout_Buttons.setObjectName(_fromUtf8("horizontalLayout_Buttons"))
        self.pushButton_Pop = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_Pop.setObjectName(_fromUtf8("pushButton_Pop"))
        self.horizontalLayout_Buttons.addWidget(self.pushButton_Pop)
        self.pushButton_Picking = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_Picking.setObjectName(_fromUtf8("pushButton_Picking"))
        self.horizontalLayout_Buttons.addWidget(self.pushButton_Picking)
        self.pushButton_LoadConf = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_LoadConf.setObjectName(_fromUtf8("pushButton_LoadConf"))
        self.horizontalLayout_Buttons.addWidget(self.pushButton_LoadConf)
        self.comboBox_Text = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_Text.setObjectName(_fromUtf8("comboBox_Text"))
        self.horizontalLayout_Buttons.addWidget(self.comboBox_Text)
        self.comboBox_CameraImg = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_CameraImg.setObjectName(_fromUtf8("comboBox_CameraImg"))
        self.horizontalLayout_Buttons.addWidget(self.comboBox_CameraImg)
        self.gridLayout_MainTab1.addLayout(self.horizontalLayout_Buttons, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayoutWidget_3 = QtGui.QWidget(self.tab_2)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(-1, -1, 1151, 601))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_GL = QtGui.QVBoxLayout()
        self.verticalLayout_GL.setObjectName(_fromUtf8("verticalLayout_GL"))
        self.gridLayout_2.addLayout(self.verticalLayout_GL, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout_Main.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_Main)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1171, 27))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_Pop.setText(_translate("MainWindow", "Pop last Marker", None))
        self.pushButton_Picking.setText(_translate("MainWindow", "Apply Picking", None))
        self.pushButton_LoadConf.setText(_translate("MainWindow", "Load 2d/3d config file", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))


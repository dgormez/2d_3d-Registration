# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Apr 21 16:04:12 2015
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
        self.Tab3 = QtGui.QTabWidget(self.centralWidget)
        self.Tab3.setObjectName(_fromUtf8("Tab3"))
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
        self.pushButton_Show3DCorresp = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_Show3DCorresp.setObjectName(_fromUtf8("pushButton_Show3DCorresp"))
        self.horizontalLayout_Buttons.addWidget(self.pushButton_Show3DCorresp)
        self.pushButton_SaveConf = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_SaveConf.setObjectName(_fromUtf8("pushButton_SaveConf"))
        self.horizontalLayout_Buttons.addWidget(self.pushButton_SaveConf)
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
        self.Tab3.addTab(self.tab, _fromUtf8(""))
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
        self.Tab3.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.gridLayoutWidget = QtGui.QWidget(self.tab_3)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 177, 303))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_CalibrateCam = QtGui.QHBoxLayout()
        self.horizontalLayout_CalibrateCam.setObjectName(_fromUtf8("horizontalLayout_CalibrateCam"))
        self.gridLayout.addLayout(self.horizontalLayout_CalibrateCam, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBox_CameraNumber = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox_CameraNumber.setObjectName(_fromUtf8("comboBox_CameraNumber"))
        self.verticalLayout.addWidget(self.comboBox_CameraNumber)
        self.pushButton_Calibrate = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_Calibrate.setObjectName(_fromUtf8("pushButton_Calibrate"))
        self.verticalLayout.addWidget(self.pushButton_Calibrate)
        self.pushButton_LoadIntrinsic = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_LoadIntrinsic.setObjectName(_fromUtf8("pushButton_LoadIntrinsic"))
        self.verticalLayout.addWidget(self.pushButton_LoadIntrinsic)
        self.pushButton_saveIntrinsic = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_saveIntrinsic.setObjectName(_fromUtf8("pushButton_saveIntrinsic"))
        self.verticalLayout.addWidget(self.pushButton_saveIntrinsic)
        self.pushButton_LoadExtrinsic = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_LoadExtrinsic.setObjectName(_fromUtf8("pushButton_LoadExtrinsic"))
        self.verticalLayout.addWidget(self.pushButton_LoadExtrinsic)
        self.pushButton_SaveExtrinsic = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_SaveExtrinsic.setObjectName(_fromUtf8("pushButton_SaveExtrinsic"))
        self.verticalLayout.addWidget(self.pushButton_SaveExtrinsic)
        self.pushButton_ExtrinsicParameters = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_ExtrinsicParameters.setObjectName(_fromUtf8("pushButton_ExtrinsicParameters"))
        self.verticalLayout.addWidget(self.pushButton_ExtrinsicParameters)
        self.pushButton_ProjectTestPoint = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_ProjectTestPoint.setObjectName(_fromUtf8("pushButton_ProjectTestPoint"))
        self.verticalLayout.addWidget(self.pushButton_ProjectTestPoint)
        self.pushButton_ProjectModel = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_ProjectModel.setObjectName(_fromUtf8("pushButton_ProjectModel"))
        self.verticalLayout.addWidget(self.pushButton_ProjectModel)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.Tab3.addTab(self.tab_3, _fromUtf8(""))
        self.gridLayout_Main.addWidget(self.Tab3, 0, 0, 1, 1)
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
        self.Tab3.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_Pop.setText(_translate("MainWindow", "Pop last Marker", None))
        self.pushButton_Show3DCorresp.setText(_translate("MainWindow", "Show 3D correspondance conf Points", None))
        self.pushButton_SaveConf.setText(_translate("MainWindow", "Save 2d/3d Markers", None))
        self.pushButton_LoadConf.setText(_translate("MainWindow", "Load 2d/3d config file", None))
        self.Tab3.setTabText(self.Tab3.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.Tab3.setTabText(self.Tab3.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))
        self.pushButton_Calibrate.setText(_translate("MainWindow", "Calibrate Camera", None))
        self.pushButton_LoadIntrinsic.setText(_translate("MainWindow", "Load Intrinsic Parameters", None))
        self.pushButton_saveIntrinsic.setText(_translate("MainWindow", "Save Intrinsic Parameters", None))
        self.pushButton_LoadExtrinsic.setText(_translate("MainWindow", "Load Extrinsic Parameters", None))
        self.pushButton_SaveExtrinsic.setText(_translate("MainWindow", "Save Extrinsic Parameters", None))
        self.pushButton_ExtrinsicParameters.setText(_translate("MainWindow", "Find Extrinsic parameters", None))
        self.pushButton_ProjectTestPoint.setText(_translate("MainWindow", "Project Point for Validation", None))
        self.pushButton_ProjectModel.setText(_translate("MainWindow", "Project Model", None))
        self.Tab3.setTabText(self.Tab3.indexOf(self.tab_3), _translate("MainWindow", "Page", None))


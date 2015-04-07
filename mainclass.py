# -*- coding: utf-8 -*-

import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtOpenGL import *


from mainWindow import Ui_MainWindow

from myOwnGLWidget import GLWidget
from ImgViewerWidget import MyQGraphicsView
from objloader import OBJ

class MainWindow(QtGui.QMainWindow):

##########################################################################
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Test 2D/3D registration')

        self.initActions()
        self.initMenus()

        print self.size()
        self.ui.pushButton.clicked.connect(self.handleButton)

        self.glWidget = GLWidget(self)
        self.glWidget.setWidth(self.size().width())
        self.ui.horizontalLayout_Main.addWidget(self.glWidget)
        
        self.imgWidget2 = MyQGraphicsView(self,self.glWidget.obj)
        self.imgWidget2.setImage("tex_0.jpg")
        self.imgWidget2.set3dModel(self.glWidget.obj)
        self.ui.horizontalLayout_Main.addWidget(self.imgWidget2)
   
##########################################################################
    def handleButton(self):
        self.glWidget.colorFaces(self.imgWidget2.pickedFaces)
        print ('Hello World')

##########################################################################
    def initActions(self):
        self.exitAction = QtGui.QAction('Quit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.connect(self.exitAction, QtCore.SIGNAL('triggered()'), self.close)

        self.openAct = QtGui.QAction("&Open Image", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

##########################################################################
    def initMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.exitAction)
        fileMenu.addAction(self.openAct)

##########################################################################
    def close(self):
        QtGui.qApp.quit()

##########################################################################
    def open(self):
        self.imgWidget.open()

##########################################################################
    def eventFilter(self, event):
        print "in keyPress"
        if event.type() == QtCore.QEvent.KeyPress:
            # do some stuff ...
            keyPressEvent(self.glWidget, event)
            return True # means stop event propagation
        else:
            return QtGui.QDialog.eventFilter(self, event)

##########################################################################
    def keyPressEvent(self, e):
        print "in Key pressed "
        if e.key() == QtCore.Qt.Key_Control:
            self.glWidget.controlPressed = True
            self.imgWidget2.controlPressed = True
        if e.key() == QtCore.Qt.Key_Shift:
            self.glWidget.shiftPressed = True
            
##########################################################################
    def keyReleaseEvent(self, event):
        self.glWidget.controlPressed = False
        self.imgWidget2.controlPressed = False

########################################################################## 
def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

##########################################################################
if __name__ == '__main__':
    main()
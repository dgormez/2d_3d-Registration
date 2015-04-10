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

        #print self.size()
        self.ui.pushButton_Picking.clicked.connect(self.applyPicking)


        self.glWidget = GLWidget(self)
        self.glWidget.setWidth(self.size().width())
        #self.ui.horizontalLayout_Main.addWidget(self.glWidget)


        self.textureWidget = MyQGraphicsView(self)
        self.textureWidget.setImage("tex_0.jpg")


        self.imgCameraWidget = MyQGraphicsView(self)
        self.imgCameraWidget.isTexture = False
        self.imgCameraWidget.setImage("SDC10225.JPG")

        self.ui.verticalLayout_GL.addWidget(self.glWidget)
        self.ui.horizontalLayout_IMGs.addWidget(self.imgCameraWidget)
        self.ui.horizontalLayout_IMGs.addWidget(self.textureWidget)
        

##########################################################################
    def handleButton(self):
        self.glWidget.colorFaces(self.imgWidget2.pickedFaces)
        print ('Hello World')

##########################################################################
    def applyPicking(self):
        print "In apply Picking"
        print "Norm texture coord =  " + str(self.textureWidget.normCoordMarkers)
        material = ""

        for norm_Coord in self.textureWidget.normCoordMarkers:
            texture,norm_CoordTMP = norm_Coord
            print "norm_Coord = " + str(norm_CoordTMP)
            print "texture = " + str(texture)

            if texture == "tex_0.jpg":
                material = "material_0"

            result,idxIntersectFaces,coord3dFromNormTextCoord = self.glWidget.searchIntersectedTriangle(norm_CoordTMP,material)
            print "Face found = " + str(result) + " face = " + str(self.glWidget.obj.faces[idxIntersectFaces]) + " Coord3dFromNormTextCoord = " + str(coord3dFromNormTextCoord)


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
        self.textureWidget.open()


##########################################################################

    def eventFilter(self, event):
        #print "in keyPress in MainClass"
        if event.type() == QtCore.QEvent.KeyPress:
            # do some stuff ...
            keyPressEvent(self.imgCameraWidget, event)
            return True # means stop event propagation
        else:
            return QtGui.QDialog.eventFilter(self, event)

##########################################################################
    def keyPressEvent(self, e):
        print "in Key pressed"
        if e.key() == QtCore.Qt.Key_Control:
            self.imgCameraWidget.controlPressed = True
            self.textureWidget.controlPressed = True
        #if e.key() == QtCore.Qt.Key_Shift:
            #self.glWidget.shiftPressed = True
            
##########################################################################
    def keyReleaseEvent(self, event):
        #self.glWidget.controlPressed = False
        self.imgCameraWidget.controlPressed = False
        self.textureWidget.controlPressed = False

##########################################################################
    def establish2d3dMarkersFrom2Dpicking(self, text_coord, camera_coord):
        """
        1) convert text_coord in 3D model cooordinates
        2) make links between camera coord and 3D coord
        """


########################################################################## 
def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

##########################################################################
if __name__ == '__main__':
    main()
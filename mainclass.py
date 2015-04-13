# -*- coding: utf-8 -*-

import sys
import numpy

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
        
        self.correspondance2D3D = []

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Test 2D/3D registration')

        self.initActions()
        self.initMenus()

        #print self.size()
        self.ui.pushButton_Picking.clicked.connect(self.applyPicking)
        self.ui.pushButton_LoadConf.clicked.connect(self.loadConfigFile)

        """
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
        """

##########################################################################
    def handleButton(self):
        self.glWidget.colorFaces(self.imgWidget2.pickedFaces)
        print ('Hello World')

##########################################################################
    def applyPicking(self):
        """
        Makes the link between the texture coord and the 3d coordinates.
        It writes the output in a file to allow a loading of a config file for the 2d/3D mapping.
        """

        f = open('2d3dMapping.conf','w')

        print "In apply Picking"
        print "Norm texture coord =  " + str(self.textureWidget.normCoordMarkers)
        material = ""

        if len(self.textureWidget.normCoordMarkers) != len(self.imgCameraWidget.coordMarkers):
            print "Markers list lengths do NOT match!!! "

        for idxCoord,norm_Coord in enumerate(self.textureWidget.normCoordMarkers):
            texture,norm_CoordTMP = norm_Coord
            imgCamera, coordImgTMP = self.imgCameraWidget.coordMarkers[idxCoord]

            print "norm_Coord = " + str(norm_CoordTMP)
            print "texture = " + str(texture)

            if texture == "tex_0.jpg":
                material = "material_0"

            result,idxIntersectFaces,coord3dFromNormTextCoord = self.glWidget.searchIntersectedTriangle(norm_CoordTMP,material)
            print "Face found = " + str(result) + " face = " + str(self.glWidget.obj.faces[idxIntersectFaces]) + " Coord3dFromNormTextCoord = " + str(coord3dFromNormTextCoord)

            arrayCoordImgTMP = self.convertQpointFToArray(coordImgTMP)
            print "arrayCoordImgTMP" + str(arrayCoordImgTMP)
            print "arrayCoordImgTMP[0]" + str(arrayCoordImgTMP[0])
            string = imgCamera + "!" + str(arrayCoordImgTMP[0])+"/"+str(arrayCoordImgTMP[1])+ "!" + str(coord3dFromNormTextCoord[0])+"/"+str(coord3dFromNormTextCoord[1])+"/"+str(coord3dFromNormTextCoord[2])
            f.write(string + '\n')
            print string
            #Add here the creation of config File

        f.close()

        print "End of Aplly Picking"
        
        return

##########################################################################
    def loadConfigFile(self):
        print "In loadConfigFile"
        filename="2d3dMapping.conf"


        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split('!',2)
            if not values: continue

            print "values = " + str(values)
            print type(values)
            print len(values)
            print "values[0] " + str(values[0])
            print "values[1] " + str(values[1])
            print "values[2] " + str(values[2])


            imgCoord = numpy.zeros(2)
            modelCoord = numpy.zeros(3)

            l=[]
            for i in range(1,3):
                for t in values[i].split():
                    idx=0
                    print "t = " +str(t)
                    #t = t.translate(None, '[]')
                    t2 = t.split('/')
                    print "t2 = " +str(t2)
                    
                    if len(t2) == 2:
                        imgCoord[0] = t2[0]
                        imgCoord[1] = t2[1]

                    if len(t2) == 3:
                        modelCoord[0] = t2[0]
                        modelCoord[1] = t2[1]
                        modelCoord[2] = t2[2]


            print imgCoord
            print modelCoord

            self.correspondance2D3D.append((values[0],imgCoord,modelCoord))

        print correspondance2D3D

##########################################################################
    def convertQpointFToArray(self,point):
            coord = numpy.zeros(2)
            coord[0] = int(point.x())
            coord[1] = int(point.y())
            print "Coordinates = " + str(coord)

            return coord

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
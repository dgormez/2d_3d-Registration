# -*- coding: utf-8 -*-

import sys
import numpy
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtOpenGL import *

from mainWindow import Ui_MainWindow
from myOwnGLWidget import GLWidget
from ImgViewerWidget import MyQGraphicsView
from objloader import OBJ
from CameraIntrinsicParamCalibration import CameraIntrinsicCalibration
from CameraExtrensicParam import CameraExtrinsicParameters
from mapping2d3d import Mapping2d3D

class MainWindow(QtGui.QMainWindow):

##########################################################################
    def __init__(self):
        super(MainWindow, self).__init__()
        self.camera_port = 1
        self.correspondance2D3D = []

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Test 2D/3D registration')
        
        self.initActions()
        self.initMenus()

        #print self.size()
        self.ui.pushButton_Picking.clicked.connect(self.applyPicking)
        self.ui.pushButton_LoadConf.clicked.connect(self.loadConfigFile)
        self.ui.pushButton_Calibrate.clicked.connect(self.intrinsicCalibration)
        self.ui.pushButton_saveIntrinsic.clicked.connect(self.saveIntrinsic)
        self.ui.pushButton_ExtrinsicParameters.clicked.connect(self.computeExtrinsicParameter)
        self.ui.pushButton_SaveValidation.clicked.connect(self.saveValidation)
        self.ui.pushButton_ProjectTestPoint.clicked.connect(self.retroProjectionTest)

        self.ui.pushButton_ProjectModel.clicked.connect(self.mapp3DModelto2D)
        
        self.ui.pushButton_LoadIntrinsic.clicked.connect(self.loadIntrinsicCameraParam)
        self.ui.pushButton_LoadExtrinsic.clicked.connect(self.loadExtrinsicCameraParam)
        self.ui.pushButton_SaveExtrinsic.clicked.connect(self.saveExtrinsic)

        self.glWidget = GLWidget(self)
        self.glWidget.setWidth(self.size().width())
        #self.ui.horizontalLayout_Main.addWidget(self.glWidget)


        self.textureWidget = MyQGraphicsView(self)
        self.textureWidget.setImage("tex_0.jpg")


        self.imgCameraWidget = MyQGraphicsView(self)
        self.imgCameraWidget.isTexture = False
        #self.imgCameraWidget.setImage("SDC10225.JPG")
        self.imgCameraWidget.setImage("BucheLogitech.jpg")

        self.ui.verticalLayout_GL.addWidget(self.glWidget)
        self.ui.horizontalLayout_IMGs.addWidget(self.imgCameraWidget)
        self.ui.horizontalLayout_IMGs.addWidget(self.textureWidget)

        self.cameraMatrix = 0
        self.dist_coefs = 0
        self.rvec = 0
        self.tvec = 0


##########################################################################
    def saveValidation(self):
        """
        Makes the link between the texture coord and the 3d coordinates.
        It writes the output in a file containing a real 2d/3d correspondance
        """

        f = open('projectPointValidation.conf','w')

        print "In apply Picking"
        #print "Norm texture coord =  " + str(self.textureWidget.normCoordMarkers)
        material = ""

        if len(self.textureWidget.normCoordMarkers) != len(self.imgCameraWidget.coordMarkers):
            print "Markers list lengths do NOT match!!! "

        for idxCoord,norm_Coord in enumerate(self.textureWidget.normCoordMarkers):
            texture,norm_CoordTMP = norm_Coord
            imgCamera, coordImgTMP = self.imgCameraWidget.coordMarkers[idxCoord]

            #print "norm_Coord = " + str(norm_CoordTMP)
            #print "texture = " + str(texture)

            if texture == "tex_0.jpg":
                material = "material_0"

            result,idxIntersectFaces,coord3dFromNormTextCoord = self.glWidget.searchIntersectedTriangle(norm_CoordTMP,material)
            #print "Face found = " + str(result) + " face = " + str(self.glWidget.obj.faces[idxIntersectFaces]) + " Coord3dFromNormTextCoord = " + str(coord3dFromNormTextCoord)

            arrayCoordImgTMP = self.convertQpointFToArray(coordImgTMP)
            #print "arrayCoordImgTMP" + str(arrayCoordImgTMP)
            #print "arrayCoordImgTMP[0]" + str(arrayCoordImgTMP[0])
            string = imgCamera + "!" + str(arrayCoordImgTMP[0])+"/"+str(arrayCoordImgTMP[1])+ "!" + str(coord3dFromNormTextCoord[0])+"/"+str(coord3dFromNormTextCoord[1])+"/"+str(coord3dFromNormTextCoord[2])
            f.write(string + '\n')
            print string
            #Add here the creation of config File

        f.close()

##########################################################################
    def retroProjectionTest(self):
        "In Test Retro projection Point"
        imgTmp, coord = self.imgCameraWidget.testProjection[0]
        #print coord
        #point = numpy.zeros(2)
        #point[0] = coord.x()
        #point[1] = coord.y()
        #print point

        self.determine3DcorrespondingPointFrom2DImage(coord)

##########################################################################
    def mapp3DModelto2D(self):
        "In Test Project Point"
        #Add a get of the current camera port
        mapping = Mapping2d3D()
        mapping.setIntrinsicParam(self.cameraMatrix,self.dist_coefs)
        mapping.setExtrinsicParam(self.rvec,self.tvec)

        self.mappingOf3DVertices = []
        self.distanceOfMappedPoints = []

        #print self.glWidget.obj.vertices[0]

        for point3D in self.glWidget.obj.vertices:

            #print type(point3D)
            #print len(point3D)
            #print point3D
            mapped2D,distToCamera = mapping.projectPoint(point3D)
            self.mappingOf3DVertices.append(mapped2D)
            self.distanceOfMappedPoints.append(distToCamera)

        print len(self.mappingOf3DVertices)
        print self.mappingOf3DVertices[0]
        print "Min Distance = ", min(self.distanceOfMappedPoints)
        print "Max Distance = ", max(self.distanceOfMappedPoints)

##########################################################################
    def determineMeanDistanceToCamera(self,current_img):
        #Remark: If i always project the hole model, then the correct projected point is the one with the smallest dist to camera
        #The mean is computed to be sure that the correct projected pixel is considered
        for projectedPoints in self.mappingOf3DVertices:
            print "determine Mean"

##########################################################################
    def determine3DcorrespondingPointFrom2DImage(self,point2D_fromImage_clicked):
        #Find the closest Points projected on the 2D image. In a radius of 5 pixels from the clicked points
        print "In determine 3D corresponding points"
        closestPoints2D =[]
        closestPointsIn3D = []
        #print type(point2D_fromImage_clicked)

        NPpoint2D_fromImage_clicked = numpy.zeros(2)
        NPpoint2D_fromImage_clicked[0] = 320
        NPpoint2D_fromImage_clicked[1] = 240

        for idx,point in enumerate(self.mappingOf3DVertices):
            #coordMapped3DVertice = numpy
            if self.isInCircle(5,NPpoint2D_fromImage_clicked,point):
                closestPoints2D.append((point,self.distanceOfMappedPoints[idx]))
                closestPointsIn3D.append(self.glWidget.obj.vertices[idx])

        print closestPoints2D
        print closestPointsIn3D

##########################################################################
    def isInCircle(self,radius,center,point):
        result = False
        #print center
        #print type(center)
        #print len(center)
        #print type(point)
        #print point.shape
        #print point[0]
        #print center.shape
        #print center[0]

        #point is very ugly but it works
        test = math.sqrt(((point[0][0][0] - center[0]) *(point[0][0][0] - center[0]) )
                + ((point[0][0][1] - center[1]) * (point[0][0][1] - center[1]) ))

        if test < radius:
            result = True

        return result

##########################################################################
    def loadIntrinsicCameraParam(self,camera_port):
        print "In load CameraParameters in CameraExtrinsicParameters"
        pathToFolder = "./CameraParameters/"

        stringIntrinsic = pathToFolder +"intrinsiCameraMatrix" + str(self.camera_port) + ".npy"
        stringDistCoef = pathToFolder+ "cameraDist_coefs" + str(self.camera_port) +".npy"
        
        self.cameraMatrix = numpy.load(stringIntrinsic)
        self.dist_coefs = numpy.load(stringDistCoef)

        print "self.cameraMatrix= " , self.cameraMatrix
        print "self.dist_coefs= " , self.dist_coefs

        return self.cameraMatrix,self.dist_coefs

##########################################################################
    def loadExtrinsicCameraParam(self):
        print "In load CameraParameters in CameraExtrinsicParameters"
        pathToFolder = "./CameraParameters/"

        stringRvec = pathToFolder +"rvec" + str(self.camera_port) + ".npy"
        stringTvec = pathToFolder+ "tvec" + str(self.camera_port) +".npy"
        
        self.rvec = numpy.load(stringRvec)
        self.tvec = numpy.load(stringTvec)

        print "rvec = " , self.rvec
        print "tvec = " , self.tvec

        return self.rvec,self.tvec

##########################################################################
    def handleButton(self):
        self.glWidget.colorFaces(self.imgWidget2.pickedFaces)
        print ('Hello World')

##########################################################################
    def intrinsicCalibration(self):
        "Allows the retrieval of the intrinsic parameters of the Camera"
        #Needs to add a get camera port from the combo Box
        self.cameraCalib = CameraIntrinsicCalibration(self.camera_port)

##########################################################################
    def saveIntrinsic(self):
        self.cameraCalib.saveParameters()

##########################################################################
    def saveExtrinsic(self):
        self.cameraCalib.saveParameters()

##########################################################################
    def computeExtrinsicParameter(self):
        print "In compute CameraExtrinsicParameters In MainClass"

        print self.correspondance2D3D
        #points2D,points3D = self.correspondingPointsPerImage("SDC10225.JPG")
        #points2D,points3D = self.correspondingPointsPerImage("SDC10225.JPG")
        
        points2D,points3D = self.correspondingPointsPerImage("BucheLogitech.jpg")
        points2D,points3D = self.correspondingPointsPerImage("BucheLogitech.jpg")

        print len(points2D)
        print len(points3D)

        self.cameraCalib = CameraExtrinsicParameters(self.camera_port)
        self.cameraCalib.loadIntrinsicCameraParam()
        self.cameraCalib.setCorrespondingPoints(points2D,points3D)
        self.cameraCalib.computeExtrensicParameters()
        self.cameraCalib.saveParameters()

##########################################################################
    def applyPicking(self):
        """
        Makes the link between the texture coord and the 3d coordinates.
        It writes the output in a file to allow a loading of a config file for the 2d/3D mapping.
        """

        f = open('2d3dMapping.conf','w')

        print "In apply Picking"
        #print "Norm texture coord =  " + str(self.textureWidget.normCoordMarkers)
        material = ""

        if len(self.textureWidget.normCoordMarkers) != len(self.imgCameraWidget.coordMarkers):
            print "Markers list lengths do NOT match!!! "

        for idxCoord,norm_Coord in enumerate(self.textureWidget.normCoordMarkers):
            texture,norm_CoordTMP = norm_Coord
            imgCamera, coordImgTMP = self.imgCameraWidget.coordMarkers[idxCoord]

            #print "norm_Coord = " + str(norm_CoordTMP)
            #print "texture = " + str(texture)

            if texture == "tex_0.jpg":
                material = "material_0"

            result,idxIntersectFaces,coord3dFromNormTextCoord = self.glWidget.searchIntersectedTriangle(norm_CoordTMP,material)
            #print "Face found = " + str(result) + " face = " + str(self.glWidget.obj.faces[idxIntersectFaces]) + " Coord3dFromNormTextCoord = " + str(coord3dFromNormTextCoord)

            arrayCoordImgTMP = self.convertQpointFToArray(coordImgTMP)
            #print "arrayCoordImgTMP" + str(arrayCoordImgTMP)
            #print "arrayCoordImgTMP[0]" + str(arrayCoordImgTMP[0])
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

            #print "values = " + str(values)
            #print type(values)
            #print len(values)
            #print "values[0] " + str(values[0])
            #print "values[1] " + str(values[1])
            #print "values[2] " + str(values[2])


            imgCoord = numpy.zeros(2)
            modelCoord = numpy.zeros(3)

            l=[]
            for i in range(1,3):
                for t in values[i].split():
                    idx=0
                    #print "t = " +str(t)
                    #t = t.translate(None, '[]')
                    t2 = t.split('/')
                    #print "t2 = " +str(t2)
                    
                    if len(t2) == 2:
                        imgCoord[0] = t2[0]
                        imgCoord[1] = t2[1]

                    if len(t2) == 3:
                        modelCoord[0] = t2[0]
                        modelCoord[1] = t2[1]
                        modelCoord[2] = t2[2]


            #print imgCoord
            #print modelCoord

            self.correspondance2D3D.append((values[0],imgCoord,modelCoord))

        print self.correspondance2D3D

##########################################################################
    def correspondingPointsPerImage(self,image):
        points2D = []
        points3D = []

        for correspondance in self.correspondance2D3D:
            img, coord2D, coord3D = correspondance
            if (img == image):
                points2D.append(coord2D)
                points3D.append(coord3D)


        return points2D,points3D

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
        if e.key() == QtCore.Qt.Key_Alt:
            self.imgCameraWidget.altPressed = True
            #self.textureWidget.controlPressed = True
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
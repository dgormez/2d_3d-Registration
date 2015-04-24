import sys
import numpy
import math
import glob

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

        self.getTextureImageList()


        #print self.size()
        self.ui.pushButton_SaveConf.clicked.connect(self.save2d3DConf)
        #self.ui.pushButton_Show3DCorresp.clicked.connect(self.showConf)
        self.ui.pushButton_LoadConf.clicked.connect(self.loadConfigFile)
        self.ui.pushButton_Calibrate.clicked.connect(self.intrinsicCalibration)
        self.ui.pushButton_saveIntrinsic.clicked.connect(self.saveIntrinsic)
        self.ui.pushButton_ExtrinsicParameters.clicked.connect(self.computeExtrinsicParameter)
        #self.ui.pushButton_SaveValidation.clicked.connect(self.saveValidation)
        self.ui.pushButton_ProjectTestPoint.clicked.connect(self.retroProjectionTest)
        self.ui.pushButton_Show3DCorresp.clicked.connect(self.showConf)
        self.ui.pushButton_ProjectModel.clicked.connect(self.mapp3DModelto2D)
        
        self.ui.pushButton_LoadIntrinsic.clicked.connect(self.loadIntrinsicCameraParam)
        self.ui.pushButton_LoadExtrinsic.clicked.connect(self.loadExtrinsicCameraParam)
        self.ui.pushButton_SaveExtrinsic.clicked.connect(self.saveExtrinsic)
        self.ui.pushButton_showSelectedImages.clicked.connect(self.showSelectedImages)


        self.glWidget = GLWidget(self)
        self.glWidget.setWidth(self.size().width())
        #self.ui.horizontalLayout_Main.addWidget(self.glWidget)


        self.textureWidget = MyQGraphicsView(self)
        #self.textureWidget.setImage("tex_0.jpg")
        self.textureWidget.setWidth(self.size().width()/2-20)

        self.imgCameraWidget = MyQGraphicsView(self)
        self.imgCameraWidget.isTexture = False
        #self.imgCameraWidget.setImage("SDC10225.JPG")
        #self.imgCameraWidget.setImage("BucheLogitech.jpg")
        #self.imgCameraWidget.setImage("SANY0011.JPG")
        #self.imgCameraWidget.setImage("DSC00388.JPG")
        
        #self.imgCameraWidget.setImage("pic00000.JPG")
        self.imgCameraWidget.setWidth(self.size().width()/2-20)
        self.showSelectedImages()
        
        self.ui.verticalLayout_GL.addWidget(self.glWidget)
        self.ui.horizontalLayout_IMGs.addWidget(self.imgCameraWidget)
        self.ui.horizontalLayout_IMGs.addWidget(self.textureWidget)

        self.cameraMatrix = 0
        self.dist_coefs = 0
        self.rvec = 0
        self.tvec = 0

##########################################################################
    def showSelectedImages(self):
        print "In show Selected Images"
        #imgCamera = self.ui.comboBox_CameraImg.itemData(self.ui.comboBox_CameraImg.currentIndex()).toString().toUtf8().constData()
        #imgTexture = self.ui.comboBox_Text.itemData(self.ui.comboBox_Text.currentIndex()).toString()

        imgCamera = str(self.ui.comboBox_CameraImg.currentText())
        imgTexture = str(self.ui.comboBox_Text.currentText())
        
        print str(self.ui.comboBox_Text.currentText())

        print "imgCamera = " + imgCamera 
        print "imgTexture = " + imgTexture

        self.imgCameraWidget.setImage(imgCamera)
        self.textureWidget.setImage(imgTexture)

        for idx,img in enumerate(self.Config_Camera_Images):
            if imgCamera == img:
                self.camera_port = idx

        return

##########################################################################
    def saveValidation(self):
        """
        Makes the link between the texture coord and the 3d coordinates.
        It writes the output in a file containing a real 2d/3d correspondance
        """

        f = open('projectPointValidation.conf','w')

        print "In save Validation"
        #print "Norm texture coord =  " + str(self.textureWidget.normCoordMarkers)
        material = ""

        if len(self.textureWidget.normCoordMarkers) != len(self.imgCameraWidget.coordMarkers):
            print "Markers list lengths do NOT match!!! "

        for idxCoord,norm_Coord in enumerate(self.textureWidget.normCoordMarkers):
            texture,norm_CoordTMP = norm_Coord
            imgCamera, coordImgTMP = self.imgCameraWidget.coordMarkers[idxCoord]

            #print "norm_Coord = " + str(norm_CoordTMP)
            #print "texture = " + str(texture)

            if texture == "./3DModelOBJ/tex_0.jpg":
                material = "Texture_0"

            if texture == "./3DModelOBJ/tex_1.jpg":
                material = "Texture_1"

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

###################################################################################
    def showConf(self):
        print "in show conf"
        self.facesCorrespondingTo2DconfigPoints = numpy.load("2d3dMappingFacesIdx.conf.npy")

        for idx,faceIdx in enumerate(self.facesCorrespondingTo2DconfigPoints):
            #print int(faceIdx)
            self.facesCorrespondingTo2DconfigPoints[idx] = int(faceIdx)
            #print self.facesCorrespondingTo2DconfigPoints[idx]
            
        print self.facesCorrespondingTo2DconfigPoints

        self.glWidget.colorFaces(self.facesCorrespondingTo2DconfigPoints)

###################################################################################
    def retroProjectionTest(self):
        "In Test Retro projection Point"
        imgTmp, coord = self.imgCameraWidget.testProjection[0]
        #print coord
        #point = numpy.zeros(2)
        #point[0] = coord.x()
        #point[1] = coord.y()
        #print point

        closestPointsIn3D, finalGuessOnCorrectPoint = self.determine3DcorrespondingPointFrom2DImage(coord)
        
        """
        for point3D in closestPointsIn3D:
            coord3D,idxVertice = point3D
            self.glWidget.colorFaceContainingVertice(idxVertice)
        """
        print "finalGuessOnCorrectPoint = " + str(finalGuessOnCorrectPoint)

        for point in finalGuessOnCorrectPoint:
            coord3D,idxVertice = point
            self.glWidget.colorFaceContainingVertice(idxVertice)
        
        self.glWidget.obj.genOpenGLList()

        print "End Retro projection"

        return

###################################################################################
    def mapp3DModelto2D(self):
        "In Test Project Point"
        #Add a get of the current camera port
        mapping = Mapping2d3D()
        mapping.setIntrinsicParam(self.cameraMatrix,self.dist_coefs)
        mapping.setExtrinsicParam(self.rvec,self.tvec)

        self.mappingOf3DVertices = []
        self.distanceOfMappedPoints = []

        #print self.glWidget.obj.vertices[0]

        for idx,point3D in enumerate(self.glWidget.obj.vertices):

            #print type(point3D)
            #print len(point3D)
            #print point3D
            mapped2D,distToCamera = mapping.projectPoint(point3D)
            self.mappingOf3DVertices.append(mapped2D)
            self.distanceOfMappedPoints.append(distToCamera)

        print len(self.mappingOf3DVertices)
        print type(self.mappingOf3DVertices)


        print self.mappingOf3DVertices[0], " is projection of " , self.glWidget.obj.vertices[0]
        print "Min Distance = ", min(self.distanceOfMappedPoints)
        print "Max Distance = ", max(self.distanceOfMappedPoints)


###################################################################################
    def determineMeanDistanceToCamera(self,current_img):
        #Remark: If i always project the hole model, then the correct projected point is the one with the smallest dist to camera
        #The mean is computed to be sure that the correct projected pixel is considered
        for projectedPoints in self.mappingOf3DVertices:
            print "determine Mean"

##########################################################################
    def determine3DcorrespondingPointFrom2DImage(self,point2D_fromImage_clicked,radius =2):
        #Find the closest Points projected on the 2D image. In a radius of 5 pixels from the clicked points
        print "In determine 3D corresponding points"
        closestPoints2D =[]
        closestPointsIn3D = []
        distancesToCamera = []

        print type(point2D_fromImage_clicked)
        print point2D_fromImage_clicked
        print len(self.mappingOf3DVertices)
        #print self.mappingOf3DVertices[0]
        print len (self.glWidget.obj.vertices)

        """
        for i in range(len (self.glWidget.obj.vertices)):
            #print self.mappingOf3DVertices[i]
            if self.mappingOf3DVertices[i][0][0][0] > 0 and self.mappingOf3DVertices[i][0][0][1] > 0 and self.mappingOf3DVertices[i][0][0][0] < 5000 and self.mappingOf3DVertices[i][0][0][1] < 5000:
                print self.mappingOf3DVertices[i]

        print "Begin Tests"

        
        center_Test = numpy.zeros(2)
        center_Test[0] = 0
        center_Test[1] = 0

        point_Test = numpy.zeros((1,1,2))
        point_Test[0][0][0] = 1
        point_Test[0][0][0] = 1

        #print self.isInCircle(10,center_Test,point_Test)

        print "Tests Finished"
        """

        NPpoint2D_fromImage_clicked = numpy.zeros(2)
        NPpoint2D_fromImage_clicked[0] = point2D_fromImage_clicked.x()
        NPpoint2D_fromImage_clicked[1] = point2D_fromImage_clicked.y()
        #print NPpoint2D_fromImage_clicked

        for idx,point in enumerate(self.mappingOf3DVertices):
            #coordMapped3DVertice = numpy

            if self.isInCircle(radius,NPpoint2D_fromImage_clicked,point):
                print "In Circle!!"
                closestPoints2D.append(point)
                closestPointsIn3D.append((self.glWidget.obj.vertices[idx+1],idx+1))#Or no +1???
                distancesToCamera.append(self.distanceOfMappedPoints[idx])
        print "Closest projected point from  "+ str(NPpoint2D_fromImage_clicked) +" Is : " +str(closestPoints2D)
        print "Corresponding to this 3d model point = " + str(closestPointsIn3D)

        idxClosest3DToCamera = self.findMostProbable3dCorrespondanceFromProjectedPoints(distancesToCamera)
        print "idxClosest3DToCamera = " +str(idxClosest3DToCamera)
        print "Distance to camera for that point = " + str(distancesToCamera[idxClosest3DToCamera])
        final3DCorrespondingPointGuess = []
        final3DCorrespondingPointGuess.append(closestPointsIn3D[idxClosest3DToCamera])
        print "final3DCorrespondingPointGuess = " + str(final3DCorrespondingPointGuess)

        return closestPointsIn3D,final3DCorrespondingPointGuess

##########################################################################
    def findMostProbable3dCorrespondanceFromProjectedPoints(self,distancesToCamera):
        print " max(distancesToCamera) " + str(max(distancesToCamera))
        print " min(distancesToCamera) " + str(min(distancesToCamera))
        #Why is it Max and not Min distance???????????
        return distancesToCamera.index(max(distancesToCamera))

##########################################################################
    def distance(self,point1,point2):
        dist = 0
        for i in range(0,len(point1)):
            dist += (point1[i] - point2[i])^2

        return math.sqrt(dist)

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
        self.camera_port = self.ui.comboBox_CameraNumber.currentIndex() + 1 

        print type(self.camera_port)
        print self.camera_port

        self.cameraCalib = CameraIntrinsicCalibration(self.camera_port)


##########################################################################
    def saveIntrinsic(self):
        self.cameraCalib.saveParameters()

##########################################################################
    def saveExtrinsic(self):
        self.cameraCalibExt.saveParameters()

##########################################################################
    def computeExtrinsicParameter(self):
        print "In compute CameraExtrinsicParameters In MainClass"

        print self.correspondance2D3D
        #points2D,points3D = self.correspondingPointsPerImage("SDC10225.JPG")
        #points2D,points3D = self.correspondingPointsPerImage("SDC10225.JPG")
        
        #points2D,points3D = self.correspondingPointsPerImage("BucheLogitech.jpg")
        #points2D,points3D = self.correspondingPointsPerImage("BucheLogitech.jpg")

        #points2D,points3D = self.correspondingPointsPerImage("DSC00388.JPG")
        #points2D,points3D = self.correspondingPointsPerImage("SANY0011.JPG")
        self.camera_port = self.ui.comboBox_CameraNumber.currentIndex() + 1
        
        for idx,img in enumerate(self.Config_Camera_Images):
            print img
            points2D,points3D = self.correspondingPointsPerImage(img)

            print len(points2D)
            print len(points3D)

            self.cameraCalibExt = CameraExtrinsicParameters(self.camera_port)
            self.cameraCalibExt.loadIntrinsicCameraParam()
            self.cameraCalibExt.setCorrespondingPoints(points2D,points3D)
            self.cameraCalibExt.computeExtrensicParameters()
            self.cameraCalibExt.saveParameters()

##########################################################################
    def save2d3DConf(self):
        """
        Makes the link between the texture coord and the 3d coordinates.
        It writes the output in a file to allow a loading of a config file for the 2d/3D mapping.
        """

        f = open('2d3dMapping.conf','w')

        print "In save 2d 3d config()"
        #print "Norm texture coord =  " + str(self.textureWidget.normCoordMarkers)
        material = ""
        string = ""
        self.facesCorrespondingTo2DconfigPoints = []

        if len(self.textureWidget.normCoordMarkers) != len(self.imgCameraWidget.coordMarkers):
            print "Markers list lengths do NOT match!!! "

        for idxCoord,norm_Coord in enumerate(self.textureWidget.normCoordMarkers):
            texture,norm_CoordTMP = norm_Coord
            imgCamera, coordImgTMP = self.imgCameraWidget.coordMarkers[idxCoord]

            #print "norm_Coord = " + str(norm_CoordTMP)
            print "texture = " + str(texture)
            print "imgCamera = " + str(imgCamera)

            if texture == "./3DModelOBJ/tex_0.jpg":
                material = "Texture_0"
            if texture == "./3DModelOBJ/tex_1.jpg":
                material = "Texture_1"
            if texture == "./3DModelOBJ/tex_2.jpg":
                material = "Texture_2"

            result,idxIntersectFaces,coord3dFromNormTextCoord = self.glWidget.searchIntersectedTriangle(norm_CoordTMP,material)
            print "Face found = " + str(result) + " face = " + str(self.glWidget.obj.faces[idxIntersectFaces]) + " Coord3dFromNormTextCoord = " + str(coord3dFromNormTextCoord)
            print "material = " + str(material)
            print "Norm Texture coord = " + str(norm_CoordTMP)

            arrayCoordImgTMP = self.convertQpointFToArray(coordImgTMP)

            print coord3dFromNormTextCoord
            if result == False:
                string = imgCamera + "!" + str(arrayCoordImgTMP[0])+"/"+str(arrayCoordImgTMP[1])+ "!" + "Probleme" #will be modified if a 3D corresponding point is found
                print "Pas de correspondance 3D trouvee!!!"
            else:
                #print "arrayCoordImgTMP" + str(arrayCoordImgTMP)
                #print "arrayCoordImgTMP[0]" + str(arrayCoordImgTMP[0])
                #print "coord3dFromNormTextCoord" + str(coord3dFromNormTextCoord)
                string = imgCamera + "!" + str(arrayCoordImgTMP[0])+"/"+str(arrayCoordImgTMP[1])+ "!" + str(coord3dFromNormTextCoord[0])+"/"+str(coord3dFromNormTextCoord[1])+"/"+str(coord3dFromNormTextCoord[2])
                self.facesCorrespondingTo2DconfigPoints.append(idxIntersectFaces)
            f.write(string + '\n')
            print string
            #Add here the creation of config File

        f.close()

        self.saveIdxConfFaces()
        print "End of save conf 2D 3D"
        
        return

##########################################################################
    def saveIdxConfFaces(self):
        length = len(self.facesCorrespondingTo2DconfigPoints)

        faces = numpy.zeros(length)
        for i in range(0,length):
            faces[i] = self.facesCorrespondingTo2DconfigPoints[i]

        filename="2d3dMappingFacesIdx.conf"
        numpy.save(filename,faces)

##########################################################################
    def loadIdxConfFaces(self):
        self.facesCorrespondingTo2DconfigPoints = numpy.load("2d3dMappingFacesIdx.conf.npy")
        print self.facesCorrespondingTo2DconfigPoints

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

        #self.loadIdxConfFaces()

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
        #self.textureWidget.open()
        return

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
    def getTextureImageList(self):
        self.Texture_images = glob.glob('./3DModelOBJ/*.jpg')
        print type(self.Texture_images)
        self.ui.comboBox_Text.clear()
        self.ui.comboBox_Text.addItems(self.Texture_images)
        #print type(Texture_images)
        #print Texture_images[0]
        self.Config_Camera_Images = glob.glob('./Acquisitions/Calibration/*.JPG')
        self.ui.comboBox_CameraImg.addItems(self.Config_Camera_Images)

        self.cameraList = []
        for i in range(1,6):
            #print i
            self.cameraList.append(str(i))

        print type(self.cameraList)

        self.ui.comboBox_CameraNumber.clear()
        self.ui.comboBox_CameraNumber.addItems(self.cameraList)

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
def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

##########################################################################
if __name__ == '__main__':
    main()
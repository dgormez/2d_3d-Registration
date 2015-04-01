from PyQt4 import QtCore, QtGui
import math
import numpy

class MyQGraphicsView(QtGui.QGraphicsView):
    #########################################################################
    def __init__(self ,parent = None):
        QtGui.QGraphicsView.__init__(self)
        #super(MyQGraphicsView, self).mouseMoveEvent(event)
        self.path = "test.png"

        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setRenderHints(QtGui.QPainter.Antialiasing)
        self.altPressed = False
        self.middlePressed = False
        self.rightPressed = False

        self.pixmap = QtGui.QPixmap()
        self.pixmap.load(self.path)
        #self.pixmap = self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.graphicsPixmapItem = QtGui.QGraphicsPixmapItem(self.pixmap)

        self.graphicsScene = QtGui.QGraphicsScene()
        self.graphicsScene.addItem(self.graphicsPixmapItem)

        self.setScene(self.graphicsScene)
        self.controlPressed = False

        print ("Size Pixmap: H = %d , W= %d"%(self.pixmap.size().height(),self.pixmap.size().width()))
    
    #########################################################################
    def set3dModel(self,model):
        self.obj3D = model

    #########################################################################
    def setImage(self,path):
        print "In set Image"
        self.path = path
        self.pixmap = QtGui.QPixmap()
        self.pixmap.load(self.path)
        self.graphicsPixmapItem = QtGui.QGraphicsPixmapItem(self.pixmap)
        self.graphicsScene = QtGui.QGraphicsScene()
        self.graphicsScene.addItem(self.graphicsPixmapItem)
        self.setScene(self.graphicsScene)

    #########################################################################
    def wheelEvent(self, event):
        self.newScale(event.delta(), 1.15,)

    #########################################################################
    def mousePressEvent(self, event):
        self._dragPos = event.pos()

        if event.button() == QtCore.Qt.MidButton:
            print"MidButton"
            self.middlePressed = True

        if event.button() == QtCore.Qt.RightButton:
            self.rightPressed = True
            print "RightButton"

        if event.button() == QtCore.Qt.LeftButton:
            self.leftPressed = True
            mouseClick = numpy.zeros(2)
            mouseClick[0] = event.pos().x()
            mouseClick[1] = event.pos().y()
            norm_coord = self.convertToTextureCoord(mouseClick)
            self.searchIntersectedTriangle(norm_coord)
            print "Left Button"


        print "mouse Pressed"
        self.getPos(event)
    
    #########################################################################
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            self.middlePressed = False
        if event.button() == QtCore.Qt.RightButton:
            self.rightPressed = False

        self.controlPressed = False
        print "mouseReleased"

    #########################################################################
    def mouseMoveEvent(self, event):
        print "In mouse move"
        if self.altPressed:
            newPos = event.pos()

            if self.middlePressed:
                diff = newPos - self._dragPos
                self._dragPos = newPos
                QApplication.setOverrideCursor(Qt.ClosedHandCursor)
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
                event.accept()
            if self.rightPressed:
                diff = newPos - self._dragPos
                self._dragPos = newPos
                QApplication.setOverrideCursor(Qt.SizeAllCursor)
                self.newScale(diff.x(), 1.01)

    #########################################################################
    def keyPressEvent(self, event):
        print"Key pressed in IMG Viewer"
        if (event.type()==QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Control):
            self.controlPressed = True

        if (event.type()==QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Shift):
            self.shiftPressed = True
            print "shift Pressed"

        #else:
            #QWidget.keyPressEvent(self, event)

    #########################################################################
    def newScale(self, operator, factor):
        if operator > 0:
            self.scale(factor, factor)
        if operator < 0:
            self.scale(1.0/factor, 1.0/factor)

    #########################################################################
    def getPos(self , event):
        position = numpy.zeros(2)
        position[0] = event.pos().x()
        position[1] = event.pos().y()

        pos =  self.mapToScene( event.pos() ) #Needs to verify if coord 0 < x < width ....
        
        print pos
        self.convertToTextureCoord(position)
        return pos

    #########################################################################
    def convertToTextureCoord(self,pos):

        norm_Coord = numpy.zeros(2)
        norm_Coord[0] = pos[0] *1.0 / self.pixmap.size().width() 
        norm_Coord[1] = pos[1] *1.0 / self.pixmap.size().height()
        print "Normalized Coordinates = " + str(norm_Coord[0]) + " , " + str(norm_Coord[1])

        return norm_Coord

    #########################################################################
    def convertToImageCoord(self,pos):

        img_Coord = numpy.zeros(2)
        img_Coord[0] = pos[0] *1.0 * self.pixmap.size().width() 
        img_Coord[1] = pos[1] *1.0 * self.pixmap.size().height()
        print "Normalized Coordinates = " + str(img_Coord[0]) + " , " + str(img_Coord[1])

        return norm_Coord

    #########################################################################
    def searchIntersectedTriangle(self,norm_point):
        "Search if norm_point lies in a face of the OBJ model"

        for idx,face in enumerate(self.obj3D.faces):
            vertices, normals, texture_coords, material = face
            verticesTextureTriangle = []#Because i m looking in the texture image and not the 3D model
            for i in range(0,len(texture_coords)):
                verticesTextureTriangle.append(self.obj3D.texcoords[texture_coords[i]])

            if self.pointInTriangle(norm_point,verticesTextureTriangle[0],verticesTextureTriangle[1],verticesTextureTriangle[2]):
                return True,idx

        return False,-1

    #########################################################################
    def sameSide(self,p1,p2, a,b):
        cp1 = numpy.cross(self.vector2D(b,a), self.vector2D(p1,a))
        cp2 = numpy.cross(self.vector2D(b,a), self.vector2D(p2,a))

        if numpy.dot(cp1, cp2) >= 0:
            return True
        else:
            return False

    #########################################################################
    def pointInTriangle(p, a,b,c):
        "Check if point lies inside a triangle defined by a,b,c"
        if (self.sameSide(p,a, b,c) and self.sameSide(p,b, a,c) and self.sameSide(p,c, a,b)):
            return True
        else:
            return False

    #########################################################################
    def vector2D(self,b,c):
        a = numpy.zeros(2)
        
        "a = b - c "
        a[0] = b[0] - c[0]
        a[1] = b[1] - c[1]

        #print ("a = %s, b= %s , c= %s"%(a,b,c))
        return a

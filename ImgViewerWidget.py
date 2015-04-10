from PyQt4 import QtCore, QtGui
import math
import numpy
import cv2

class MyQGraphicsView(QtGui.QGraphicsView):

    #########################################################################
    def __init__(self ,parent = None):
        QtGui.QGraphicsView.__init__(self)
        #super(MyQGraphicsView, self).mouseMoveEvent(event)
        self.path = "test.png"

        #self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setRenderHints(QtGui.QPainter.Antialiasing)
        self.altPressed = False
        self.middlePressed = False
        self.rightPressed = False

        self.pixmap = QtGui.QPixmap()
        self.pixmap.load(self.path)


        #self.pixmap = self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        
        self.graphicsPixmapItem = QtGui.QGraphicsPixmapItem(self.pixmap)
        self.graphicsScene = QtGui.QGraphicsScene()
        self.graphicsScene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.graphicsScene.addItem(self.graphicsPixmapItem)
        #self.imItem = self.graphicsScene.addPixmap(self.pixmap)
        self.setScene(self.graphicsScene)

        self.controlPressed = False
        self.obj3D = obj
        self.pickedFaces = []
        print ("Size Pixmap: H = %d , W= %d"%(self.pixmap.size().height(),self.pixmap.size().width()))

        
        img = cv2.imread("tex_0.jpg")
        self.imgOriginal = img


        self.coordMarkers = []
        self.normCoordMarkers = []

    #########################################################################
    def wheelEvent(self, event):
        self.newScale(event.delta(), 1.15,)

    #########################################################################
    def mousePressEvent(self, event):
        print "mouse Pressed"
        self._dragPos = event.pos()

        if event.button() == QtCore.Qt.MidButton:
            #print"MidButton"
            self.middlePressed = True

        if event.button() == QtCore.Qt.RightButton:
            self.rightPressed = True
            #print "RightButton"

        if event.button() == QtCore.Qt.LeftButton:
            #print "Left Button"
            if self.controlPressed == True : 
                self.leftPressed = True
                
                print "self.coordMarkers = " + str(self.coordMarkers)
                mappedMouseClick = self.getPosRelativeToScene(event)
                self.coordMarkers.append(mappedMouseClick)
                norm_coord = self.convertToTextureCoord(mappedMouseClick)
                self.normCoordMarkers.append(norm_coord)
                #result,idx = self.searchIntersectedTriangle(norm_coord) # return result,idxIntersectFaces
                #self.pickedFaces = idx
                #print ("Triangle found = "+ str(result) + " and face index = " + str(idx)) #return result,idxIntersectFaces

                img_cv_Marked = self.drawCircles(self.imgOriginal)
                pix_updated = self.convertImgToPixmap(img_cv_Marked)
                self.updatePixmap(pix_updated)

        #self.getPos(event)

    #########################################################################
    def updatePixmap (self,pixmap):
        print "In update Pixmap"

        """
        pix = QtGui.QPixmap()
        pix.load("test.png")
        """

        self.graphicsScene = QtGui.QGraphicsScene()
        self.graphicsPixmapItem = QtGui.QGraphicsPixmapItem(pixmap)
        self.graphicsPixmapItem.setPixmap(pixmap)
        self.graphicsScene.addItem(self.graphicsPixmapItem)
        self.setScene(self.graphicsScene)
        #self.graphicsScene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        
        print "Exit update Pixmap"
        return

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
    def getPosRelativeToScene(self , event):
        pos =  self.mapToScene( event.pos() ) #Needs to verify if coord 0 < x < width ....        
        print "position = " + str(pos)

        return pos

    #########################################################################
    def convertToTextureCoord(self, pos):
        norm_Coord = numpy.zeros(2)
        norm_Coord[0] = pos.x() *1.0 / self.pixmap.size().width()
        norm_Coord[1] = 1- ((pos.y()) *1.0 / self.pixmap.size().height())
        print "Event position = " + str(pos)
        print "Pixmap Size = " + str(self.pixmap.size())
        print "Mouse position = " + str(pos)
        print "Normalized Coordinates = " + str(norm_Coord[0]) + " , " + str(norm_Coord[1])

        return norm_Coord



    #########################################################################
    def convertToImageCoord(self,pos):
        img_Coord = numpy.zeros(2)
        img_Coord[0] = pos[0] *1.0 * self.pixmap.size().width() 
        img_Coord[1] = pos[1] *1.0 * self.pixmap.size().height()

        print "Normalized Coordinates = " + str(img_Coord[0]) + " , " + str(img_Coord[1])

        return norm_Coord

    """

    If button Pop last pressed:
        self.coordMarkers.pop()

    """

    #########################################################################
    def convertImgToPixmap(self,cv_img):
        #if cv_img != None:
        # Notice the dimensions.
        height, width, bytesPerComponent = cv_img.shape
        bytesPerLine = bytesPerComponent * width;

        # Convert to RGB for QImage.
        cv2.cvtColor(cv_img, cv2.cv.CV_BGR2RGB,cv_img)

        image = QtGui.QImage(cv_img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(image)

        return pix

    
    #########################################################################
    def drawCircles(self,img):
        print "In draw Circles"
        print self.coordMarkers
        imgMarked = numpy.copy(img)

        for i in range (0,len(self.coordMarkers)):
            cv2.circle(imgMarked,(int(self.coordMarkers[i].x()),int(self.coordMarkers[i].y())), 10, (0,0,255), -1)

        #cv2.imshow("window",imgMarked)
        return imgMarked

    
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
    def sameSide(self,p1,p2, a,b):
        cp1 = numpy.cross(self.vector2D(b,a), self.vector2D(p1,a))
        cp2 = numpy.cross(self.vector2D(b,a), self.vector2D(p2,a))

        if numpy.dot(cp1, cp2) >= 0:
            return True
        else:
            return False

    #########################################################################
    def pointInTriangle(self,p, a,b,c):
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

    #########################################################################
    #This function should be moved in myOwnGlWidget
    def searchIntersectedTriangle(self,norm_point,img_texture="material_0"):
        "Search if norm_point lies in a face of the OBJ model"
        result = False
        idxIntersectFaces = []

        for idx,face in enumerate(self.obj3D.faces):
            vertices, normals, texture_coords, material = face
            verticesTextureTriangle = []#Because i m looking in the texture image and not the 3D model
            
            if material == img_texture:
                for i in range(0,len(texture_coords)):
                    
                    verticesTextureTriangle.append(self.obj3D.texcoords[texture_coords[i]-1])

                
                if self.pointInTriangle(norm_point,verticesTextureTriangle[0],verticesTextureTriangle[1],verticesTextureTriangle[2]):
                    print "Corresponding Face = " + str(face)
                    idxIntersectFaces.append(idx)
                    result = True
                

        return result,idxIntersectFaces


    """
    #########################################################################
    def pointInTriangleBarycenter(self,vertices,norm_point_click):
        result = False
        #Compute barycentric coordinates
        p_x  = norm_point_click[0]
        p_y  = norm_point_click[1]

        #print vertices
        #print vertices[0]
        #print vertices[0][0]

        p1_x = vertices[0][0]
        p1_y = vertices[0][1]
        p2_x = vertices[1][0]
        p2_y = vertices[1][1]
        p3_x = vertices[2][0]
        p3_y = vertices[2][1]


        #point p1(x1, y1);
        #point p2(x2, y2);
        #point p3(x3, y3);

        #point p(x,y); // <-- You are checking if this point lies in the triangle.


        alpha = ((p2_y - p3_y)*(p_x - p3_x) + (p3_x - p2_x)*(p_y - p3_y)) *1.0 / ((p2_y - p3_y)*(p1_x - p3_x) + (p3_x - p2_x)*(p1_y - p3_y))
        beta = ((p3_y - p1_y)*(p_x - p3_x) + (p1_x - p3_x)*(p_y - p3_y)) *1.0 /  ((p2_y - p3_y)*(p1_x - p3_x) + (p3_x - p2_x)*(p1_y - p3_y))
        gamma = 1.0 - alpha - beta

        if ((alpha > 0) and (beta > 0) and (gamma > 0)) :
            result =  True

        if result:
            print alpha
            print (("Alpha = %f beta = %f gamma = %f")%(alpha,beta,gamma))

        return result
        """
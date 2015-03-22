import sys
import math 
import numpy 

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
from numpy import array

from objloader import OBJ


class GLWidget(QtOpenGL.QGLWidget):
    xRotationChanged = QtCore.pyqtSignal(int)
    yRotationChanged = QtCore.pyqtSignal(int)
    zRotationChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__()
        self.parent = parent
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #self.setFocus(QtCore.Qt.MouseFocusReason)
        #Place super constructor of super-class __init__() of type GLWidget
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.height = self.size().height()
        self.width = self.size().width()
        #self.resize(800,800) #To do because of bad geometry
        print str(self.size())
        print (str(self.height))
        print(str(self.width))
        #Problem with size???


        self.yRotDeg = 0.0
        self.isPressed = False
        self.controlPressed = False
        self.shiftPressed = False

        self.oldx = self.oldy = 0
        self.setMouseTracking(True)


        self.rx, self.ry ,self.rz= (0,0,0)
        self.tx, self.ty = (0,0)
        self.zpos = 5
        self.rotate = self.move = False

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0,  150))


        #glEnable(GL_DEPTH_TEST)
           # most obj files expect to be smooth-shaded

        self.obj = OBJ("3D_360Recap_8Mpx_JPG_CLEANED_FULLY.obj")
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.fovy = 90.0
        self.aspect = self.width / float(self.height)
        self.zNear = 1.0
        self.zFar = 100.0
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)#????
        glShadeModel(GL_SMOOTH)


    def resizeGL(self, width, height):
        self.height = width
        self.width = height
        print (str(self.height) + str(self.width))
        side = min(width, height)
        if side < 0:
            return

        glViewport(0, 0,self.height, self.width)
        #glViewport((width - side) / 2, (self.height - side) / 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width / float(self.height)
        
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        #glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        glMatrixMode(GL_MODELVIEW)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        """
        # RENDER OBJECT
        glTranslate(self.tx/20., self.ty/20., self.zpos)
        glRotate(self.ry, 1, 0, 0)
        glRotate(self.rx, 0, 1, 0)
        glRotate(self.rz, 0, 0, 1)
        glCallList(self.obj.gl_list)
        """

        glTranslated(self.tx, self.ty, -self.zpos)
        glRotate(self.xRot, 1.0, 0.0, 0.0)
        glRotate(self.yRot , 0.0, 1.0, 0.0)
        glRotate(self.zRot , 0.0, 0.0, 1.0)
        glCallList(self.obj.gl_list)

    def mouseMoveEvent(self, mouseEvent):
        if self.controlPressed:
            self.rotate = False

        if int(mouseEvent.buttons()) != QtCore.Qt.NoButton :
            # user is dragging
            delta_x = mouseEvent.x() - self.oldx
            delta_y = mouseEvent.y() - self.oldy 
            print "self.controlPressed = " + str(self.controlPressed)
            print "self.rotate = " + str(self.rotate)
            if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton :
                if self.rotate : 
                    #self.rx += delta_x
                    self.setXRotation(self.xRot + delta_y)
                    self.setYRotation(self.yRot + delta_x)
                    #self.ry += delta_y
            elif int(mouseEvent.buttons()) & QtCore.Qt.RightButton :
                #self.camera.translateSceneRightAndUp( delta_x, delta_y )
                if self.rotate :
                    self.setXRotation(self.xRot + delta_y)
                    self.setZRotation(self.zRot + delta_x)
                    #self.rz +=  delta_x
                if self.controlPressed : 
                #if self.move : 
                    self.tx += delta_x/10
                    self.ty += -delta_y/10

            self.update()

        self.oldx = mouseEvent.x()
        self.oldy = mouseEvent.y()


    def wheelEvent(self, event):
        x = event.delta()
        #d = - float(_event.delta()) / 200.0 * self.radius_
        #self.updateGL()
        self.zpos += 2 * math.copysign(1, x)
        print "wheelEvent x = ", x
        self.update()

    def mouseDoubleClickEvent(self, mouseEvent):
        print "double click"

    def mousePressEvent(self, e):
        print "mouse press"
        self.isPressed = True
        self.lastPos = e.pos()
        if int(e.buttons()) & QtCore.Qt.LeftButton : self.rotate = True
        if int(e.buttons()) & QtCore.Qt.RightButton : self.move = True

        if int(e.buttons()) & QtCore.Qt.LeftButton :
            if self.shiftPressed == True:
                self.pick(e.pos())
                self.pickRay(e.pos())

    def mouseReleaseEvent(self, e):
        print "mouse release"
        if int(e.buttons()) & QtCore.Qt.LeftButton : self.rotate = False
        if int(e.buttons()) & QtCore.Qt.RightButton : self.move = False
        self.isPressed = False

    def keyPressEvent(self, event):
        print"key pressed"
        if (event.type()==QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Control):
            self.controlPressed = True

        if (event.type()==QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Shift):
            self.shiftPressed = True
            print "shift Pressed"

        else:
            QWidget.keyPressEvent(self, event)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

#launch a ray and see with triangle it intersects


    def pick(self, pos):
        print "In pick"
        glInitNames()
        glSelectBuffer(64)
        glRenderMode(GL_SELECT)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        viewport = glGetIntegerv(GL_VIEWPORT)
        #n_w,n_h = display._screen.dimensions
        #glOrtho(-n_w,n_w,-n_h,n_h,1,0)

        print "viewport = " 
        print viewport
        print pos
        print "pos x = " + str(pos.x()) 
        self.aspect = self.width / float(self.height)
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        
        GLU.gluPickMatrix(pos.x(),viewport[3]-pos.y(),3,3,viewport)
        glMatrixMode(GL_MODELVIEW)

        #for index, i in enumerate(self.items):
        #    glPushName(index)

        print "About to leave Pick()"

    def pickRay(self,position):
        print "In PickRay()"
        window_width = self.width
        window_height = self.height
        aspect = (window_width)/(window_height)
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()

        near_height = 2 * 1.0 * math.tan(self.fovy/2)
        zNear = 1.0
        zFar = 100.0
        glFrustum(-near_height * self.aspect, near_height * self.aspect, - near_height, near_height, self.zNear, self.zFar )

        window_y = (window_height - position.y()) - window_height/2
        norm_y = window_y/(window_height/2)
        window_x = position.x() - window_width/2
        norm_x = window_x/(window_width/2)

        y = near_height * norm_y
        x = near_height * aspect * norm_x

        """
        To transform this eye coordinate pick ray into object coordinates, multiply it by the inverse of the ModelView matrix in use when the scene was rendered. 
        When performing this multiplication, remember that the pick ray is made up of a vector and a point, and that vectors and points transform differently. 

        You can translate and rotate points, but vectors only rotate.
        """
        ray_pnt = (0.0, 0.0, 0.0, 1.0)
        ray_vec = (x, y, -near_distance, 0.0)

        # your pick ray vector is (x, y, -zNear).
        #retrieve current modelVieuw Matrix
        glGetFloatv (GL_MODELVIEW_MATRIX, mvmatrix)
        print mvmatrix

        inv_matrix = numpy.mvmatrix.I
        "Leaves pickRay"

#http://svn.navi.cx/misc/trunk/pybzengine/BZEngine/UI/ThreeDRender/Engine.py
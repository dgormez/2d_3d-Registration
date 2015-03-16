import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
from numpy import array

from objloader import OBJ


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.height = self.size().height()
        self.width = self.size().width()
        print str(self.size())
        self.yRotDeg = 0.0
        

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0,  150))


        #glEnable(GL_DEPTH_TEST)
        #glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

        self.obj = OBJ("3D_360Recap_8Mpx_JPG_CLEANED_FULLY.obj")
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width / float(self.height)
        GLU.gluPerspective(90.0, aspect, 1.0, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)


    def resizeGL(self, width, height):
        self.height = width
        self.width = height

        if self.height == 0: self.height = 1

        glViewport(0, 0,self.height, self.width)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width / float(self.height)
        
        GLU.gluPerspective(90, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
 
        rx, ry = (0,0)
        tx, ty = (0,0)
        zpos = 5
        rotate = move = False


        # RENDER OBJECT
        glTranslate(tx/20., ty/20., - zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        glCallList(self.obj.gl_list)

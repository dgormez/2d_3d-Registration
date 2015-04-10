import sys
import math 
import numpy 
import time

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

    #########################################################################
    def __init__(self, parent=None):
        super(GLWidget, self).__init__()
        self.parent = parent
        #print "parent = " + str(parent)
        
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #self.setFocus(QtCore.Qt.MouseFocusReason)
        #Place super constructor of super-class __init__() of type GLWidget
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.height = self.size().height()
        self.width = self.size().width()
        #self.resize(800,800) #To do because of bad geometry
        #print str(self.size())

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

        #self.obj = OBJ("3D_360Recap_8Mpx_JPG_CLEANED_FULLY.obj")
        self.lastPos = QtCore.QPoint()

        #self.initializeGL()


    #########################################################################
    #This function should be moved in myOwnGlWidget
    def searchIntersectedTriangle(self,norm_point,img_texture="material_0"):
        "Search if norm_point lies in a face of the OBJ model"
        result = False
        idxIntersectFaces = -1
        coord3dFromNormTextCoord = -1
        print "In searchIntersectedTriangle" 
        print "norm_point = " + str(norm_point)

        for idx,face in enumerate(self.obj.faces):
            vertices, normals, texture_coords, material = face
            verticesTextureTriangle = []#Because i m looking in the texture image and not the 3D model
            
            if material == img_texture:
                for i in range(0,len(texture_coords)):
                    
                    verticesTextureTriangle.append(self.obj.texcoords[texture_coords[i]-1])

                
                if self.pointInTriangle(norm_point,verticesTextureTriangle[0],verticesTextureTriangle[1],verticesTextureTriangle[2]):
                    print "Corresponding Face = " + str(face)
                    print "Vertices = " + str(vertices)
                    v1,v2,v3 = vertices
                    #print "Type v1 =" + str(type(v1))
                    #print "Vertices extraction = " + str(v1) + " " + str(v2)
                    #print "self.obj.vertices = "  + str(self.obj.vertices[0])
                    idxIntersectFaces = idx
                    real3DVertices = []
                    real3DVertices.append(self.obj.vertices[v1-1])
                    real3DVertices.append(self.obj.vertices[v2-1])
                    real3DVertices.append(self.obj.vertices[v3-1])
                    coord3dFromNormTextCoord = self.centerTriangle(real3DVertices)
                    result = True
                

        return result,idxIntersectFaces,coord3dFromNormTextCoord

    def centerTriangle(self,vertices):
        "Simple average of Points in the Triangle. Could be replaced with the exact selected point in texture_coords (and its equivalent in the 3D model)"
        print "In centerTriangle()"
        center = numpy.zeros(3)
        print "Vertices = " + str(vertices)

        center[0] = (vertices[0][0] + vertices[0][1] + vertices[0][2]) *1.0 / 3
        center[1] = (vertices[1][0] + vertices[1][1] + vertices[2][2]) *1.0 / 3
        center[2] = (vertices[2][0] + vertices[2][1] + vertices[2][2]) *1.0 / 3

        print "Center = " + str(center)
        return center


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



#############################################################################
    def setWidth(self,width):
        self.setMinimumSize(width/2, 200)

#############################################################################
    def setModel(self,obj):
        self.obj = obj

#############################################################################
    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0,  150))
        self.obj = OBJ("3D_360Recap_8Mpx_JPG_CLEANED_FULLY.obj")
        #glEnable(GL_DEPTH_TEST)
           # most obj files expect to be smooth-shaded

        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.fovy = 60.0
        self.aspect = self.width / float(self.height)
        self.zNear = 1.0
        self.zFar = 40.0
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        self.near_height = 2 * 1.0 * math.tan(self.fovy/2)

        #glFrustum(-self.near_height * self.aspect,
        #            self.near_height * self.aspect, -self.near_height, self.near_height, self.zNear, self.zFar )
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

#############################################################################
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
        self.aspect = self.width / float(self.height)
        
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        #glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        #glFrustum(-self.near_height * self.aspect,
                    #self.near_height * self.aspect, -self.near_height, self.near_height, self.zNear, self.zFar )
        glMatrixMode(GL_MODELVIEW)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
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
            #print "self.rotate = " + str(self.rotate)
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
        #print "wheelEvent x = ", x
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
            if self.shiftPressed:
                #self.pick(e.pos())
                """
                #Test 3D picking
                vector_pickRay,point_pickray = self.pickRay(e.pos())
                vectorRay,originRay = self.mouseRay(e.pos())
                vectorRay2,originRay2 = self.mouseRay2(e.pos())
                vector_pickRay2,point_pickray2 = self.pickRay2(e.pos())
                vector_pickRay3,point_pickray3 = self.pickRay3(e.pos())
                collision, face = self.obj.testIntersection(vectorRay,originRay)
                collision2, face2 = self.obj.testIntersection(vector_pickRay,point_pickray)
                collision3, face3 = self.obj.testIntersection(vectorRay2,originRay2)
                collision4, face4 = self.obj.testIntersection(vector_pickRay2,point_pickray2)
                collision5, face5 = self.obj.testIntersection(vector_pickRay3,point_pickray3)

                if collision:
                    print "collision 1 [mouseRay()] Succeded" + str (face)
                if collision2:
                    print "collision 2 [pickRay()] Succeded" + str (face2)
                    for faceToColor in face2:
                        color = 'Red'
                        print "face2 = " + str(faceToColor)
                        print "Type = " +str(type(faceToColor))
                        #self.obj.extendColor(faceToColor,color)
                        self.obj.colorFace(faceToColor,color,True)
                if collision3:
                    print "Collision 3 mouseRay2() Succeded "  + str (face3)
                if collision4:
                    print "Collision 4 [pickRay2()] Succeded "  + str (face4)
                if collision5:
                    print "Collision 5 [pickRay3()] Succeded "  + str (face5)
                """
    
    #########################################################################
    def mouseReleaseEvent(self, e):
        print "mouse release"
        if int(e.buttons()) & QtCore.Qt.LeftButton : self.rotate = False
        if int(e.buttons()) & QtCore.Qt.RightButton : self.move = False
        self.isPressed = False
        self.shiftPressed = False

    #########################################################################
    def keyPressEvent(self, event):
        print"key pressed"
        if (event.type()==QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Control):
            self.controlPressed = True

        if (event.type()==QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Shift):
            self.shiftPressed = True
            #print "shift Pressed"

        else:
            QWidget.keyPressEvent(self, event)


    #########################################################################
    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()
    

    #########################################################################
    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()


    #########################################################################
    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()

    #########################################################################
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle
    #launch a ray and see with triangle it intersects


    
    #########################################################################
    def vector(self,b,c):
        "Makes a vector from two points"
        a = numpy.zeros(3)
        "a = b - c "
        a[0] = b[0] - c[0]
        a[1] = b[1] - c[1]
        a[2] = b[2] - c[2]

        return a

    #########################################################################
    def normalize(self,a):
        TmpSum = 0
        for i in range(0,len(a)):
            TmpSum += a[i] * a[i]

        normFactor =  math.sqrt(TmpSum)

        return (a /normFactor)

    #########################################################################
    def colorMousePicking(self):
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_FOG)
        glDisable(GL_LIGHTING)
        
        return

    #########################################################################
    def colorFaces(self,faces):
        print faces
        for faceIdx in faces:
            self.obj.colorFace(self.obj.faces[faceIdx],'Red')

        self.obj.genOpenGLList()

        return

#http://svn.navi.cx/misc/trunk/pybzengine/BZEngine/UI/ThreeDRender/Engine.py
    

"""
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

"""


"""
void MouseDownEvent(int x, int y)
 {
      // turn off texturing, lighting and fog
      glDisable(GL_TEXTURE_2D);
      glDisable(GL_FOG);
      glDisable(GL_LIGHTING);
 
      // render every object in our scene
      // suppose every object is stored in a list container called SceneObjects
      list<SceneObject *>::iterator itr = SceneObjects.begin();
      while(itr != SceneObjects.end())
      {
           (*itr)->Picking();
           itr++;
      }
 
      // get color information from frame buffer
      unsigned char pixel[3];
 
      GLint viewport[4];
      glGetIntegerv(GL_VIEWPORT, viewport);
 
      glReadPixels(x, viewport[3] - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE, pixel);
 
      // now our picked screen pixel color is stored in pixel[3]
      // so we search through our object list looking for the object that was selected
      itr = SceneObjects.begin();
      while(itr != SceneObjects.end())
      {
           if((*itr)->m_colorID[0] == pixel[0] && (*itr)->m_colorID[1] == pixel[1] && (*itr)->m_colorID[2] == pixel[2])
           {
                // flag object as selected
                SetSelected((*itr);
                break;
           }
           itr++;
      }
 }


"""
"""
def pickRay(self,position):
        "Creates a vectorRay computing the  inverse of the eye coordinates"
        print "In PickRay()  computing the  inverse of the eye coordinates "
        
        window_width = self.width
        window_height = self.height
        aspect = (window_width)/(window_height)

        glMatrixMode( GL_PROJECTION )
        #glLoadIdentity()

        near_height = 2 * 1.0 * math.tan(self.fovy/2)
        zNear = 1.0
        zFar = 100.0
        #glFrustum(-near_height * self.aspect, near_height * self.aspect, - near_height, near_height, self.zNear, self.zFar )
        #It maybe sets the origin of the look point. Must change.
        
        #glTranslated(self.tx, self.ty, -self.zpos)
        #glRotate(self.xRot, 1.0, 0.0, 0.0)
        #glRotate(self.yRot , 0.0, 1.0, 0.0)
        #glRotate(self.zRot , 0.0, 0.0, 1.0)

        
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)

        window_y = (window_height - position.y()) - window_height/2
        norm_y = window_y/(window_height/2)
        window_x = position.x() - window_width/2
        norm_x = window_x/(window_width/2)

        y = near_height * norm_y
        x = near_height * aspect * norm_x


        ""
        To transform this eye coordinate pick ray into object coordinates, multiply it by the inverse of the ModelView matrix in use when the scene was rendered. 
        When performing this multiplication, remember that the pick ray is made up of a vector and a point, and that vectors and points transform differently. 

        You can translate and rotate points, but vectors only rotate. You can translate and rotate points, but vectors only rotate. 
        The way to guarantee that this is working correctly is to define your point and vector as four-element arrays
        ""
        
        near_distance = self.zNear
        ray_pnt = numpy.array([0.0, 0.0, 0.0, 1.0])
        ray_vec = numpy.array([x, y, -near_distance, 0.0])
        #print "ray_pnt =" +  str(ray_pnt)
        #print "ray_vect = " + str(ray_vec)
        # your pick ray vector is (x, y, -zNear).
        #retrieve current modelVieuw Matrix
        mvmatrix = numpy.array(numpy.identity(4), copy=False)
        
        mvmatrix = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX, mvmatrix))
        #print mvmatrix

        inv_matrix = numpy.linalg.inv(mvmatrix)
        #print "Model View vmatrix  = " + str(mvmatrix)
        #print "Inverse Model View vmatrix  = " + str(inv_matrix)
        #print inv_matrix.shape
        #print ray_pnt.shape
        #print ray_vec.shape

        point_pickray = numpy.dot(ray_pnt,inv_matrix)
        vector_pickRay = numpy.dot(ray_vec,inv_matrix)

        if len(vector_pickRay) == 4:
            vector_pickRay = numpy.delete(vector_pickRay,3)

        if len(point_pickray) == 4:
            point_pickray = numpy.delete(point_pickray,3)

        print "point_pickray = " + str(point_pickray)
        print "vector_pickray = " + str(vector_pickRay)

        ""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width / float(self.height)
        
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        #glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        glMatrixMode(GL_MODELVIEW)
        ""

        return vector_pickRay,point_pickray

    def pickRay2(self,position):
        "Creates a vectorRay computing the  inverse of the eye coordinates"
        print "In PickRay()  computing the  inverse of the eye coordinates "
        
        window_width = self.width
        window_height = self.height
        aspect = (window_width)/(window_height)

        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        #glFrustum(-self.near_height * self.aspect, self.near_height * self.aspect, -self.near_height,
        #   self.near_height, self.zNear, self.zFar )


        #glFrustum(-near_height * self.aspect, near_height * self.aspect, - near_height, near_height, self.zNear, self.zFar )
        #It maybe sets the origin of the look point. Must change.
        ""
        glTranslated(self.tx, self.ty, -self.zpos)
        glRotate(self.xRot, 1.0, 0.0, 0.0)
        glRotate(self.yRot , 0.0, 1.0, 0.0)
        glRotate(self.zRot , 0.0, 0.0, 1.0)
        ""
        
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)

        window_y = (window_height - position.y()) - window_height/2
        norm_y = window_y/(window_height/2)
        window_x = position.x() - window_width/2
        norm_x = window_x/(window_width/2)

        y = self.near_height * norm_y
        x = self.near_height * aspect * norm_x


        ""
        To transform this eye coordinate pick ray into object coordinates, multiply it by the inverse of the ModelView matrix in use when the scene was rendered. 
        When performing this multiplication, remember that the pick ray is made up of a vector and a point, and that vectors and points transform differently. 

        You can translate and rotate points, but vectors only rotate. You can translate and rotate points, but vectors only rotate. 
        The way to guarantee that this is working correctly is to define your point and vector as four-element arrays
        ""
        
        near_distance = self.zNear
        ray_pnt = numpy.array([0.0, 0.0, 0.0, 1.0])
        ray_vec = numpy.array([x, y, -near_distance, 0.0])
        #print "ray_pnt =" +  str(ray_pnt)
        #print "ray_vect = " + str(ray_vec)
        # your pick ray vector is (x, y, -zNear).
        #retrieve current modelVieuw Matrix

        mvmatrix = numpy.array(numpy.identity(4), copy=False)
        mvmatrix = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX, mvmatrix))
        #print mvmatrix

        inv_matrix = numpy.linalg.inv(mvmatrix)
        #print "Model View vmatrix  = " + str(mvmatrix)
        #print "Inverse Model View vmatrix  = " + str(inv_matrix)
        #print inv_matrix.shape
        #print ray_pnt.shape
        #print ray_vec.shape

        point_pickray = numpy.dot(ray_pnt,inv_matrix)
        vector_pickRay = numpy.dot(ray_vec,inv_matrix)

        if len(vector_pickRay) == 4:
            vector_pickRay = numpy.delete(vector_pickRay,3)

        if len(point_pickray) == 4:
            point_pickray = numpy.delete(point_pickray,3)

        print "point_pickray = " + str(point_pickray)
        print "vector_pickray = " + str(vector_pickRay)

        ""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-self.near_height * self.aspect, self.near_height * self.aspect, -self.near_height,
           self.near_height, self.zNear, self.zFar )
        glMatrixMode(GL_MODELVIEW)
        ""

        return vector_pickRay,point_pickray

    def pickRay3(self,position):

        "Creates a vectorRay computing the  inverse of the eye coordinates"
        print "In PickRay3()  computing the  inverse of the eye coordinates "
        
        window_width = self.width
        window_height = self.height
        aspect = (window_width)/(window_height)

        glMatrixMode( GL_PROJECTION )
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        #glMatrixMode( GL_PROJECTION )
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        #glFrustum(-self.near_height * self.aspect, self.near_height * self.aspect, -self.near_height,
           #self.near_height, self.zNear, self.zFar )


        #glFrustum(-near_height * self.aspect, near_height * self.aspect, - near_height, near_height, self.zNear, self.zFar )
        #It maybe sets the origin of the look point. Must change.

        glTranslated(self.tx, self.ty, -self.zpos)
        glRotate(self.xRot, 1.0, 0.0, 0.0)
        glRotate(self.yRot , 0.0, 1.0, 0.0)
        glRotate(self.zRot , 0.0, 0.0, 1.0)
        
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)

        window_y = (window_height - position.y()) - window_height/2
        norm_y = window_y/(window_height/2)
        window_x = position.x() - window_width/2
        norm_x = window_x/(window_width/2)

        y = self.near_height * norm_y
        x = self.near_height * aspect * norm_x

        z_cursor = glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        print "z_cursor"  + str(z_cursor)

        ""
        To transform this eye coordinate pick ray into object coordinates, multiply it by the inverse of the ModelView matrix in use when the scene was rendered. 
        When performing this multiplication, remember that the pick ray is made up of a vector and a point, and that vectors and points transform differently. 

        You can translate and rotate points, but vectors only rotate. You can translate and rotate points, but vectors only rotate. 
        The way to guarantee that this is working correctly is to define your point and vector as four-element arrays
        ""
        
        near_distance = self.zNear
        ray_pnt = numpy.array([0.0, 0.0, 0.0, 1.0])
        ray_vec = numpy.array([x, y, -near_distance, 0.0])
        #print "ray_pnt =" +  str(ray_pnt)
        #print "ray_vect = " + str(ray_vec)
        # your pick ray vector is (x, y, -zNear).
        #retrieve current modelVieuw Matrix
        #print "Model View vmatrix  = " + str(mvmatrix)
        #print "Inverse Model View vmatrix  = " + str(inv_matrix)
        #print inv_matrix.shape

        matModelView = numpy.array(numpy.identity(4), copy=False)
        matProjection = numpy.array(numpy.identity(4), copy=False)
        viewport = numpy.zeros(4)
        #get matrix and viewport

        matModelView = glGetDoublev( GL_MODELVIEW_MATRIX)
        matProjection = glGetDoublev( GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv( GL_VIEWPORT)
        
        inv_matrix = numpy.linalg.inv(matModelView)

        transformMatrix = numpy.linalg.inv(numpy.dot(matProjection,matModelView))

        print "In paick Ray 3"
        print matModelView
        print matProjection


        point_pickray = numpy.dot(ray_pnt,transformMatrix)
        vector_pickRay = numpy.dot(ray_vec,transformMatrix)

        if len(vector_pickRay) == 4:
            vector_pickRay = numpy.delete(vector_pickRay,3)

        if len(point_pickray) == 4:
            point_pickray = numpy.delete(point_pickray,3)

        print "point_pickray = " + str(point_pickray)
        print "vector_pickray = " + str(vector_pickRay)


        return vector_pickRay,point_pickray

    def mouseRay(self,position):
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        glTranslated(self.tx, self.ty, -self.zpos)
        glRotate(self.xRot, 1.0, 0.0, 0.0)
        glRotate(self.yRot , 0.0, 1.0, 0.0)
        glRotate(self.zRot , 0.0, 0.0, 1.0)


        "Creates a vectorRay using the gluUnProject twice"
        print "In mouseRay Creating a vectorRay using the gluUnProject twice"

        matModelView = numpy.array(numpy.identity(4), copy=False)
        matProjection = numpy.array(numpy.identity(4), copy=False)
        viewport = numpy.zeros(4)
        #get matrix and viewport

        matModelView = glGetDoublev( GL_MODELVIEW_MATRIX)
        matProjection = glGetDoublev( GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv( GL_VIEWPORT)

        print ("Model Vieuw Matrix = " + str(matModelView))
        print ("Matrix Projection = " + str(matProjection))
        
        # window pos of mouse, Y is inverted on Windows
        winX = position.x() 
        #winY = viewport[3] - position.y() #we need to "invert" our MY, because in OpenGL Y axis has direction that is reverse to window Y axis
        winY = position.y() #we need to "invert" our MY, because in OpenGL Y axis has direction that is reverse to window Y axis

        p_start = numpy.zeros(3)
        p_end = numpy.zeros(3)
        # get point on the 'near' plane (third param is set to 0.0)
        p_start[0],p_start[1],p_start[2] = GLU.gluUnProject(winX, winY, 0.0, matModelView, matProjection, 
             viewport)

        #get point on the 'far' plane (third param is set to 1.0)
        p_end[0], p_end[1], p_end[2] = GLU.gluUnProject(winX, winY, 1.0, matModelView, matProjection, 
             viewport)

        # now you can create a ray from m_start to m_end
        vectorRay = self.vector(p_end,p_start)
        

        mvmatrix = numpy.array(numpy.identity(4), copy=False)
        mvmatrix = numpy.array(glGetFloatv(GL_MODELVIEW_MATRIX, mvmatrix))
        #print ("Inverse Model Vieuw Matrix = " + str(matModelView))

        inv_matrix = numpy.linalg.inv(mvmatrix)
        originRay = numpy.array([0.0,0.0,0.0,1.0])
        originRay = numpy.dot(originRay,inv_matrix)

        if len(vectorRay) == 4:
            vectorRay = numpy.delete(vectorRay,3)

        if len(originRay) == 4:
            originRay = numpy.delete(originRay,3)

        print "Vector Ray = " + str(vectorRay)
        print "Origin Ray = " + str(originRay)

        ""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width / float(self.height)
        
        GLU.gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        #glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        glMatrixMode(GL_MODELVIEW)
        ""
        return vectorRay,originRay

    def mouseRay2(self,position):
        "Creates a vectorRay using the gluUnProject once and gluReadPixels"
        print "In mouseRay Creating a vectorRay using the gluUnProject twice"
        glMatrixMode( GL_MODELVIEW ) #or GL_PROJECTION ???
        glPushMatrix()
        glLoadIdentity()
        glTranslated(self.tx, self.ty, -self.zpos)
        glRotate(self.xRot, 1.0, 0.0, 0.0)
        glRotate(self.yRot , 0.0, 1.0, 0.0)
        glRotate(self.zRot , 0.0, 0.0, 1.0)

        matModelView = numpy.array(numpy.identity(4), copy=False)
        matProjection = numpy.array(numpy.identity(4), copy=False)
        viewport = numpy.zeros(4)

        #get matrix and viewport
        matModelView = glGetDoublev( GL_MODELVIEW_MATRIX)
        matProjection = glGetDoublev( GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv( GL_VIEWPORT)
        
        transformMatrix = numpy.linalg.inv(numpy.dot(matProjection,matModelView))
        # window pos of mouse, Y is inverted on Windows
        #Viewport Coordinates
        winX = position.x() 
        winY = viewport[3] - position.y()

        #winZ = glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        


        #Normalised Device Coordinates  range [-1:1, -1:1, -1:1]
        x = 2.0 * winX / viewport[2] -1.0 #float x = (2.0f * mouse_x) / width - 1.0f;
        y = 1.0 - (2.0 * winY) / viewport[3]
        z = 1.0
        ray_nds = numpy.array([x,y,z])

        #4d Homogeneous Clip Coordinates range [-1:1, -1:1, -1:1, -1:1]
        ray_clip = numpy.array([ray_nds[0],ray_nds[1], -1.0, 1.0])

        #4d Eye (Camera) Coordinates range [-x:x, -y:y, -z:z, -w:w]
        ray_eye = numpy.dot(numpy.linalg.inv(matProjection),ray_clip)
        ray_eye = numpy.array([ray_eye[0], ray_eye[1], -1.0, 0.0])
        ray_eye_norm = self.normalize(ray_eye)


        #4d World Coordinates  range [-x:x, -y:y, -z:z, -w:w]
        ray_wor = numpy.dot(numpy.linalg.inv(matModelView),ray_eye_norm)
        #Do i need model vieuw or vieuw matrix alone????
        #Do i need to check intersection in world coord or in Object coordinates???
        ray_wor = self.normalize(ray_wor)

        p_start = numpy.zeros(3)

        return ray_wor,p_start
"""
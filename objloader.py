import pygame
from OpenGL.GL import *
import numpy 
import time




def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        #print "values MTL = " + str(values)
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
            #print "Mtl = " + str(mtl)
        elif mtl is None:
            raise ValueError, "mtl file doesn't start with newmtl stmt"
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]
            #surf = cv2.imread(mtl['map_Kd'])
            surf = pygame.image.load(mtl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            #image = pygame.image.tostring(surf, 'RGBA', 1)
            #height, width, depth = surf.shape
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
            #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, height, width, 0, GL_RGBA,
            #    GL_UNSIGNED_BYTE, surf.date)

        else:
            mtl[values[0]] = map(float, values[1:])

    return contents
 
class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        print ("Load A new instance of OBJ file")
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.uniqueID = []
        self.selectedFaces = []
        self.modifiedFaces = []
        
        self.gColorID = numpy.zeros(3)
        self.m_colorID = numpy.zeros(3)


        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'): 
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))#Add here unique ID

        #print ("Length: vertices = %s ; normals = %s ; textcoord = %s ; faces = %s " % (len(self.vertices),len(self.normals),len(self.texcoords),len(self.faces)))
        #print ("min self.face" + str(min(self.faces)))
        #print ("Shapes self.faces" + str(self.faces.shape) + "  Shapes self.vertices" + str(self.vertices.shape))
        self.gl_list = glGenLists(1)
        #print str(self.gl_list)
        glNewList(self.gl_list, GL_COMPILE)
        
        #print ("vertice [0] " + str(self.vertices[0]))
        #print( "self.texcoords[0] = " + str(self.texcoords[0]))
        #print ("self.faces[0] =" + str (self.faces[0]) )

        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face
 
            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])
                #print " mtl['Kd'] = " + mtl['Kd']
 
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()


        """
        parametric equation of the line:

        point(t) = p + t * d

        where 

        p is a point in the line
        d is a vector that provides the line's direction
        """
        
        self.redTextCoordIndex = len(self.texcoords) +1
        array = [self.redTextCoordIndex,self.redTextCoordIndex,self.redTextCoordIndex]
        #print "array = " + str(array)
        self.texcoords.append(array)
        self.texcoords.append([0.5,0.5])
        
        
        return

    def uniqueColor(self,gColorID):
        gColorID[0]+=1
        if(gColorID[0] > 255):
            gColorID[0] = 0
            gColorID[1]+=1
            if(gColorID[1] > 255):
                gColorID[1] = 0
                gColorID[2]+= 1

        return gColorID

    def addCustomColors(self):
        return


    def genOpenGLList(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)

        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face
 
            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])
                #print " mtl['Kd'] = " + mtl['Kd']
 
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()


    def genOpenGLListIDColor(self):
        self.gl_list_ColorID = glGenLists(1)
        
        glNewList(self.gl_list_ColorID, GL_COMPILE)
        
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face
 
            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])
                #print " mtl['Kd'] = " + mtl['Kd']
 
            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def rayIntersectsTriangle(self,p, d, v0, v1, v2):

        e1 = self.vector(v1,v0)
        e2 = self.vector(v2,v0)

        h = numpy.cross(d,e2)
        a = numpy.dot(e1,h)

        if (a > -0.00001 and a < 0.00001):
            return False

        f = 1/a
        s = self.vector(p,v0)
        u = f * numpy.dot(s,h)

        if (u < 0.0) or (u > 1.0):
            return False

        q = numpy.cross(s,e1)
        v = f * numpy.dot(d,q)

        if (v < 0.0) or (u + v > 1.0):
            return False

        #at this stage we can compute t to find out where
        #the intersection point is on the line
        t = f * numpy.dot(e2,q)

        if (t > 0.00001):# ray intersection
            return True
        else :
            return False # this means that there is a line intersection but not a ray intersection

    def testIntersection(self,p,d):
        print "Testing intersection with  " + str(len(self.vertices)) + " faces."
        tmps1=time.clock()
        collision = False
        facesIntersect = []
        compteur = 1



        for face in self.faces:
            verticesFace, normals, texture_coords, material = face
            #print "verticesFace[0] = " + str(verticesFace[0])

            # -1 because a valid vertex index starts with 1 and indexing is from 0
            if self.rayIntersectsTriangle(p,d,self.vertices[verticesFace[0]-1],self.vertices[verticesFace[1]-1],self.vertices[verticesFace[2]-1]):
                #print "Collision found in " + str (time.clock()-tmps1) + " seconds"
                collision = True
                facesIntersect.append(face)
            compteur +=1


        #print "Collisions = " + str(collision) + "  Found in " + str (time.clock()-tmps1)
        
        return collision,facesIntersect

    def vector(self,b,c):
        a = numpy.zeros(3)
        
        "a = b - c "
        a[0] = b[0] - c[0]
        a[1] = b[1] - c[1]
        a[2] = b[2] - c[2]
        #print ("a = %s, b= %s , c= %s"%(a,b,c))
        return a

    def colorFace(self,face,color,update = False):
        "Color selected face in color given by color parameter"
        """
        
        For each vertice, search for the faces having these vertices in common.
        Modify the texture coord and material for those vertices
        Generate a new gl_list

        
        """


        print "In colorFace()"

        idx = self.faces.index(face)
        vertices, normals, texture_coords, material = face
        self.modifiedFaces.append((vertices, normals, texture_coords, material,idx))
        array = numpy.array([self.redTextCoordIndex - 1,self.redTextCoordIndex - 1,self.redTextCoordIndex - 1])
        print array
        array.astype(numpy.uint8)

        #array = numpy.array([self.redTextCoordIndex - 1,self.redTextCoordIndex - 1,self.redTextCoordIndex - 1],dtype = numpy.uint8)
        #print "array = ",array
        #print ("Old face = " + str(face))

        if color == "Red":    
            material = 'material_4'
            texcoords = array#self.texcoords[self.redTextCoordIndex - 1 ]
            #print "texcoords = " +str(texcoords)

            ownTuple = (vertices, normals, texcoords, material)
            #print ("New face = " + str(ownTuple))
            self.faces[idx] = ownTuple
            print "In color Face(), face to color = " + str(face)
            print "After coloring, face = " + str(self.faces[idx])

        if update:
            self.genOpenGLList()


        
    def extendColor(self,face,color):
        #Si dans un certain range, modif la couleur
        #Modif en passant en coor spheriques
        print "In extend color() , face = " + str(face)
        print "Type = " +str(type(face))
        idx = self.faces.index(face)
        print "idx = " +str(idx)
        verticesInit, normals, texture_coords, material = face
        vertices = []
        verticesTmp = []
        vertices.append(verticesInit[0])
        vertices.append(verticesInit[1])
        vertices.append(verticesInit[2])

        for i in range(1,2):
            verticesTmp = vertices
            for faceCurr in self.faces:
                verticesCurr, normals, texture_coords, material = faceCurr

                if verticesCurr[0] in verticesTmp:
                    self.colorFace(faceCurr,color)
                    vertices.append(verticesCurr[1])
                    vertices.append(verticesCurr[2])
                
                elif verticesCurr[1] in verticesTmp:
                    self.colorFace(faceCurr,color)
                    vertices.append(verticesCurr[0])
                    vertices.append(verticesCurr[2])

                elif verticesCurr[2] in verticesTmp:
                    self.colorFace(faceCurr,color)
                    vertices.append(verticesCurr[0])
                    vertices.append(verticesCurr[1])

            for element in verticesTmp:
                vertices.remove(element)

            vertices = list(set(vertices)) #Remove Duplicates



        self.genOpenGLList()

        return

    def distance(self,point1,point2):
        dist = 0
        for i in range(0,len(point1)):
            dist += (point1[i] - point2[i])^2

        return math.sqrt(dist)

    def closestPoint(self,point):
        closest = 1000

        for verticesTmp in self.vertices:
            distTmp = self.distance(point,pointTmp)
            if distTmp < closest:
                closest_point = pointTmp

        idx = self.vertices.index(closest_point)

        print " point = " +str(point) + " Closest point = " + str(closest_point)
        
        return closest_point

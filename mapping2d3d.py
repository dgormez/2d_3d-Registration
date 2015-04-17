import cv2
import cv2.cv as cv    #Just a formality!
import time
import numpy
import math


class Mapping2d3D():
    """
    Projects 3D points to an image plane.

    Python: cv2.projectPoints(objectPoints, rvec, tvec, cameraMatrix, distCoeffs[, imagePoints[, jacobian[, aspectRatio]]]) Returns imagePoints, jacobian


    The function computes projections of 3D points to the image plane given intrinsic and extrinsic camera parameters. Optionally, the function computes 
    Jacobians - matrices of partial derivatives of image points coordinates (as functions of all the input parameters) with respect to the particular 
    parameters, intrinsic and/or extrinsic. The Jacobians are used during the global optimization in calibrateCamera(), solvePnP(), and stereoCalibrate(). 
    The function itself can also be used to compute a re-projection error given the current intrinsic and extrinsic parameters.
    """
    def __init__(self):
        self.objectPoints = 0
        self.rvec = 0
        self.tvec = 0
        self.cameraMatrix = 0
        self.distCoeffs = 0
        self.imagePoints = 0 
        self.jacobian = 0
        self.aspectRatio = 0

    def setIntrinsicParam(self,camera_Matrix,dist_coefs):
        print "In Set Intrinsic param in mapping 2d3d"
        
        self.cameraMatrix = camera_Matrix
        self.dist_coefs = dist_coefs

        print "self.cameraMatrix= " , self.cameraMatrix
        print "self.dist_coefs= " , self.dist_coefs

    def setExtrinsicParam(self,rvec,tvec):
        print "In Set Extrinsic param in mapping 2d3d"
        self.rvec = rvec
        self.tvec = tvec

    def projectPoint(self,point3D):
        
        """
        This function is used to project a point from the Model on the image plane.
        Doing so will allow to find the 3D equivalence of each point on the plane.
        """
        converted_Point = point3D
        #print point3D
        #print point3D.shape
        #print type(point3D)
        #print type(point3D[0])

        if isinstance(point3D, list): 
            #print "It is a List. Praise the Gods!"
            converted_Point = numpy.zeros((1,3),dtype='float32')
            converted_Point[0][0] = point3D[0]
            converted_Point[0][1] = point3D[1]
            converted_Point[0][2] = point3D[2]

        #print point3D
        #point3D.shape = (1,3)
        #print point3D.shape
        #print point3D

        imgPoint, jacobian = cv2.projectPoints(converted_Point, self.rvec, self.tvec, self.cameraMatrix, self.dist_coefs)

        #print "Model 3D point: " + str(point3D)
        #print "Image point :" + str(imgPoint)

        dist = self.computeDistance3DPointCamera(converted_Point)
        #print "distance to Camera = ", dist

        return imgPoint,dist

    def computeDistance3DPointCamera(self,point3D):
        #print point3D.shape
        #print point3D[0]

        #print self.tvec.shape
        #print self.tvec
        #print self.tvec[0][0]
        #print self.tvec[1][0]
        
        dist = math.sqrt( (point3D[0][0] - self.tvec[0][0]) * (point3D[0][0] - self.tvec[0][0]) 
                           + (point3D[0][1] - self.tvec[1][0]) * (point3D[0][1] - self.tvec[1][0])
                           + (point3D[0][2] - self.tvec[2][0]) * (point3D[0][2] - self.tvec[2][0]))
        
        return dist

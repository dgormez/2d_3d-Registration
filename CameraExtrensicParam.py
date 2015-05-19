import cv2
import cv2.cv as cv    #Just a formality!
import time
import numpy


class CameraExtrinsicParameters():
    def __init__(self,camera_Port = 0):
    	self.camera_port = camera_Port
    	self.cameraMatrix = 0
    	self.dist_coefs = 0

    	self.points2D=[]
    	self.points3D=[]

    def loadIntrinsicCameraParam(self):
    	print "In load CameraParameters in CameraExtrinsicParameters"
    	pathToFolder = "./CameraParameters/"

    	stringIntrinsic = pathToFolder +"intrinsiCameraMatrix" + str(self.camera_port) + ".npy"
        stringDistCoef = pathToFolder+ "cameraDist_coefs" + str(self.camera_port) +".npy"
        
        self.cameraMatrix = numpy.load(stringIntrinsic)
        self.dist_coefs = numpy.load(stringDistCoef)

        print "self.cameraMatrix= " , self.cameraMatrix
        print "self.dist_coefs= " , self.dist_coefs

    def setCorrespondingPoints(self,points2D,points3D):
    	print "In setCorrespondingPoints"

    	self.points2D = self.transformListInArrayOfPoints(points2D)
    	self.points3D = self.transformListInArrayOfPoints(points3D)
    	print "leave setCorrespondingPoints"

    def computeExtrensicParameters(self):
    	print "In computeExtrensicParameters"
    	errVal, self.rvec, self.tvec = cv2.solvePnP(self.points3D,self.points2D, self.cameraMatrix, self.dist_coefs)
    	print "After SolvePnP"

    	print "Err_val:" ,errVal
        print "Rvec: " , self.rvec
        print "tvec" ,self.tvec
    	
    	return errVal, self.rvec, self.tvec

    def transformListInArrayOfPoints(self,listOfPoints):
    	#print len(listOfPoints)
    	#print listOfPoints
    	#print listOfPoints[0].shape[0]
    	pointsArray = numpy.zeros((len(listOfPoints),listOfPoints[0].shape[0]))

    	for i in range(0,len(listOfPoints)):
    		for j in range(0,listOfPoints[0].shape[0]):
    			pointsArray[i,j] = listOfPoints[i][j]

    	#print pointsArray.shape

    	return pointsArray

    def saveParameters(self,filename=""):
        print "In Extrinsic Camera Parameters Saving"
        pathToFolder = "./CameraParameters/"
        stringRvec = "rvec" + str(self.camera_port)+".npy"
        stringTvec= "tvec" + str(self.camera_port)+".npy"

        numpy.save(pathToFolder + stringRvec,  self.rvec)
        numpy.save(pathToFolder + stringTvec, self.tvec)

        #print numpy.load(pathToFolder + stringIntrinsic)
        #print numpy.load(pathToFolder + stringDistCoef)

        print "End of Save Extrinsic Parameters"


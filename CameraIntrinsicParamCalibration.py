import cv2
import cv2.cv as cv    #Just a formality!
import time
import numpy


class CameraIntrinsicCalibration():
    def __init__(self,camera=1):
        # Camera 0 is the integrated web cam on my netbook
        self.camera_port = camera
        print "self.camera_port = " + str(self.camera_port)
        
        cv.NamedWindow("camera", cv.CV_WINDOW_AUTOSIZE)

        # Initialize the camera
        capture = cv.CaptureFromCAM(self.camera_port)# camera_port -> index of camera

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = numpy.zeros((7*10,3), numpy.float32) #Needs to be adjusted with the pattern Size (here 7*10).
        objp[:,:2] = numpy.mgrid[0:7,0:10].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        gray=0

        print ("Avant if")

        if capture : # Camera initialized without any errors
            i = 0
            while True:

                img = cv.QueryFrame(capture)

                cv.ShowImage("camera", img)
                #cv2.cv.SaveImage('pic{:>05}.jpg'.format(i), img)
                test_img = numpy.asarray(img[:,:])

                gray = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)

                # Find the chess board corners
                ret, corners = cv2.findChessboardCorners(gray, (7,10),None)

                # If found, add object points, image points (after refining them)
                if ret == True:
                    print "Corners found in " + str(i) +" images."
                    cv.SaveImage('./imagesCalibration/pic{:>05}.jpg'.format(i), img)
                    #print("Image saved.")
                    i += 1

                    objpoints.append(objp)

                    cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                    imgpoints.append(corners)

                    # Draw and display the corners
                    cv2.drawChessboardCorners(test_img, (7,10), corners,ret)
                    cv2.imshow('camera',test_img)
                
                cv2.waitKey(250)


                k = cv2.waitKey(15) & 0xFF
                
                if  k == ord('q'):
                    break

                if  k== ord('s'):
                    cv.SaveImage('./imagesCalibration/pic{:>05}.jpg'.format(i), img)
                    print("Image saved.")
                    i += 1

        #print type(objpoints)
        #print type(objpoints[0])
        #print objpoints[0]
        #print type(imgpoints)
        #print imgpoints[0]
        #print len(objpoints)
        #print len(imgpoints)
        #print gray.shape[::-1]

        self.rms, self.camera_matrix, self.dist_coefs, self.rvecs, self.tvecs  = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        #calibrate Camera returns the camera matrix, distortion coefficients, rotation and translation vectors 

        print "RMS:", self.rms #average re-projection error. Should be as close to 0 as possible.
        print "camera matrix:\n", self.camera_matrix
        print "distortion coefficients: ", self.dist_coefs.ravel()
        #print "Rotation vectors" ,self.rvecs
        #print "translation Vectors",self.tvecs 

        cv2.cv.DestroyWindow("camera")

        print ("Fin")

    def saveParameters(self):
        print "In Intrinsic Camera Parameters Saving"
        pathToFolder = "./CameraParameters/"
        stringIntrinsic = "intrinsiCameraMatrix" + str(self.camera_port)+".npy"
        stringDistCoef = "cameraDist_coefs" + str(self.camera_port)+".npy"

        numpy.save(pathToFolder + stringIntrinsic, self.camera_matrix)
        numpy.save(pathToFolder + stringDistCoef, self.dist_coefs)

        #print numpy.load(pathToFolder + stringIntrinsic)
        #print numpy.load(pathToFolder + stringDistCoef)

        print "End of Save Intrinsic Parameters"
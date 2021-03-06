
import numpy as np
import cv2
import cv2.aruco as aruco
import glob
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

flagShowWindow = False;
#cap = cv2.VideoCapture(0)
camera =PiCamera()
camera.resolution=(640,480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)



# termination criteria for the iterative algorithm
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# checkerboard of size (9 x 6) is used
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# iterating through all calibration images
# in the folder
images = glob.glob('calib_images/*.jpg')
# File storage in OpenCV
cv_file = cv2.FileStorage("calib_images/test.yaml", cv2.FILE_STORAGE_READ)

# Note : we also have to specify the type
# to retrieve otherwise we only get a 'None'
# FileNode object back instead of a matrix
mtx = cv_file.getNode("camera_matrix").mat()
dist = cv_file.getNode("dist_coeff").mat()
#This part is not done because it's ressource heavy and not needed since it's already done and stored in afile calib_images/test.yaml
###------------------ ARUCO TRACKER ---------------------------

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # operations on the frame
    rawCapture.truncate(0)
    rawCapture.seek(0)
    frame = frame.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # set dictionary size depending on the aruco marker selected
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # font for displaying text (below)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # check if the ids list is not empty
    # if no check is added the code will crash
    if np.all(ids != None):

        # estimate pose of each marker and return the values
        # rvet and tvec-different from camera coefficients
        rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        #(rvec-tvec).any() # get rid of that nasty numpy value array error

        for i in range(0, ids.size):
            # draw axis for the aruco markers
            aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)
            nptvec = np.array(tvec[i])#We get Translation vector of the marker of the index i
            if ids[i] == 2 and nptvec[0,2]<2:#We now check if the index is the second, and check if the translation value is smaller than 2, which is an arbitrary value
                #TODO : When calibrating we should check if the index is the correct one, in the line above, and check if the range (nptvect[0,2]) is good
                print("RED !!!!!!!")#This should be replaced by a blinking LED
#            print(rvec[i])#
#            print("Vecteur de rotation :"#TODO : Logs the values, Needed to know which value is needed for calibration
#            print("Vecteur de translation :")#Same as precedent
#            print(tvec[i])#Same as precedent
        # draw a square around the markers#Same as precedent
        aruco.drawDetectedMarkers(frame, corners)#Draws the aruco three base vectors on the marker 


      
        # code to show ids of the marker found
        strg = ''
        for i in range(0, ids.size):
            strg += str(ids[i][0])+', '

            cv2.putText(frame, "Id: " + strg, (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
#           print(str(ids[i][0]))

    else:
        # code to show 'No Ids' when no markers are found
#       print("no Ids")
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

        # display the resulting frame
               
    frame = cv2.resize(frame, (640, 480))                    # Resize image
    if flagShowWindow == True :
        cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()


# References
# 1. https://docs.opencv.org/3.4.0/d5/dae/tutorial_aruco_detection.html
# 2. https://docs.opencv.org/3.4.3/dc/dbb/tutorial_py_calibration.html
# 3. https://docs.opencv.org/3.1.0/d5/dae/tutorial_aruco_detection.html

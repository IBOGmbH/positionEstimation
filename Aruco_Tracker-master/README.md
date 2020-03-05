<img src="https://docs.opencv.org/3.1.0/markers.jpg" height="100">          <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/OpenCV_Logo_with_text.png" height="100">

# Aruco Tracker
[![HitCount](http://hits.dwyl.io/njanirudh/Aruco_Tracker.svg)](http://hits.dwyl.io/njanirudh/Aruco_Tracker)

**Aruco Tracker** is a small program written in python to find a registered aruco marker and then run a pose estimation algorithm on it, this is a modified version of njanirudh[4].

## Dependencies
* Python 3.x
* Numpy
* OpenCV 3.3+ 
* OpenCV 3.3+ Contrib modules

## Scripts
1. **camera_calibration.py** : Shows the steps required to calibrate a camera using opencv default calibration images and writes the value to a file.

2. **extract_calibration.py**  : This script shows how to open and extract the calibration values from a file.

3. **pose_estimation.py**  : Steps to extract pose of an checkerboard marker.

4. **aruco_tracker.py** : Extracts pose of multiple aruco markers from a webcam stream.

## Specific usecase : 
The first step is to take calibration pictures. 
This is done with the calibration_images/taking_pictures.sh (please delete the images before ), the checker is also included in the folder "images".
Ths script will take 25 picutes at 1.5 second interval, move the camera in random different positions (the chessboard needs to always be visible).

Once the pictures are taken, the script camera_calibration.py needs to be launched.

Now the aruco_tracker.py can be launched. 
There is a flag for having or not a GUI at the beginning of the file. 
It's adviced to print the values of the tvecs to get an idea of where the threshold should be.

Version 0.1 
Ilias
## References
1. https://docs.opencv.org/3.4.0/d5/dae/tutorial_aruco_detection.html
2. https://docs.opencv.org/3.4.3/dc/dbb/tutorial_py_calibration.html
3. https://docs.opencv.org/3.1.0/d5/dae/tutorial_aruco_detection.html
4. https://github.com/njanirudh/Aruco_Tracker


 
 
 
 

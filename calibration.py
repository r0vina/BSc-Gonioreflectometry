# Calibration of cameras using chessboard photographs, and convert to a format
# required by the Alignment script.



import sqlite3
import numpy as np
import cv2 as cv
import glob
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:6,0:9].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('../bsc/checker/*.jpg')
for fname in images:

    img = cv.imread(fname)
    #cv.imshow("img",img)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,6), None)
    #print(ret, corners)
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("True")
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (2,2), (-1,-1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (9,6), corners2, ret)

        cv.namedWindow("window", cv.WINDOW_KEEPRATIO)
        cv.imshow("window", img)
        cv.resizeWindow("window", 1200,1200)
        cv.imwrite(f'img_{fname}.jpg', img)
        cv.waitKey(500)
#cv.destroyAllWindows()

conn = sqlite3.connect("../bsc/bunny125/colmap125/cropped_lit.db")

# Get a cursor for executing queries
cur = conn.cursor()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


tx = 5.36276
ty = 0.425471
tz = -0.479603
3085.714286, 3085.714286, 2000.000000, 1500.000000
colmap_K = [[3085.714286, 0.0, 2000.0],[0.0, 3085.714286, 1500.0],[0.0,0.0,1.0]]
tvecs = [[0, 0, 0]]
rvecs = [[0.,0.,0.]]
#tvecs = [[0.,0.,0.]]
Ks = [[[0.],[0.],[0.],[0.]]]
results_dict = {'K': mtx, 'Ks': Ks, 'rvecs': rvecs, 'tvecs': tvecs}

# Save the dictionary as an npz file
np.savez('calib.npz', **results_dict)
print("ret:", ret, "mtx", mtx, "dist", dist, "rvecs", rvecs, "tvecs", tvecs)
print(cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None))

qx = 0.95876554161206595
qy = -0.006807590925575562
qz = 0.24606570272612466
qw = 0.14203507617842295

tx = -4.1542952427458921
ty = -1.8110962852217176
tz = 2.9380196363915263

quaternion = np.array([qx, qy, qz, qw])
#rvecs, _ = cv.Rodrigues(quaternion)

print(rvecs)

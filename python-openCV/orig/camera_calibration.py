import cv2
import numpy as np

from find_chessboard import find_chessboard

def visualize_distortion(camera_matrix, dist_coefs, (width, height), alpha=0.0):
    camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs,
                                                    (width, height), alpha)
    
    img = np.ones((height, width), dtype=np.uint8) * 255
    for y in range(0, height, 10):
        cv2.line(img, (0, y), (width - 1, y), (0, 0, 0))
    for x in range(0, width, 10):
        cv2.line(img, (x, 0), (x, height - 1), (0, 0, 0))
    img = cv2.undistort(img, camera_matrix, dist_coefs)
    cv2.imshow("Distortion with alpha="+str(alpha), img)


if __name__ == '__main__':
    obj_points = []
    img_points = []
    
    for i in range(1,3):
        img = cv2.imread("../images/chessboard%i.jpg" % i)
        h,w = img.shape[:2]
        
        found, result_img, pattern_points, corner_points = find_chessboard(img, square_size=0.05, pattern_size=(9, 6))
        if found:
            obj_points.append(pattern_points)
            img_points.append(corner_points)
            
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h))
    
    print "RMS:", rms
    print "camera matrix:\n", camera_matrix
    print "distortion coefficients: ", dist_coefs
    print
    
    
    h,w = img.shape[:2]
    visualize_distortion(camera_matrix, dist_coefs, (w, h), alpha=0.0)
    visualize_distortion(camera_matrix, dist_coefs, (w, h), alpha=1.0)
    
    #
    # Now some undistort methods for the last image
    #
    
    # undistort the last image
    distorted_img = img
    img_points = img_points[-1]
    obj_points = obj_points[-1]
    rvec = rvecs[-1]
    tvec = tvecs[-1]
    
    opt_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), alpha=0)
    undistorted_img = cv2.undistort(distorted_img, opt_camera_matrix, dist_coefs)
    
    # version 1, using world coordinates, distorted image, calibrated camera matrix and distortion coefficients
    points, _ = cv2.projectPoints(obj_points, rvec, tvec, camera_matrix, dist_coefs)
    for point in points:
        point = np.rint(point.flatten()).astype(int)
        red_color = (0, 0, 255)
        cv2.circle(distorted_img, tuple(point), 2, red_color, -1)
        
    # version 2, using world coordinates, undistorted image, calibrated camera matrix and empty distortion coefficients
    empty_dist_coefs = np.array([[0.0, 0.0, 0.0, 0.0, 0.0]])
    points, _ = cv2.projectPoints(obj_points, rvec, tvec, camera_matrix, empty_dist_coefs)
    for point in points:
        point = np.rint(point.flatten()).astype(int)
        blue_color = (255, 0, 0)
        cv2.circle(undistorted_img, tuple(point), 2, blue_color, -1)
        
    # version 3, using image coordinates, undistorted image, calibrated camera matrix and distortion coefficients
    for point in img_points:
        point = cv2.undistortPoints(np.array([[point]]), camera_matrix, dist_coefs, P=camera_matrix)
        point = np.rint(point.flatten()).astype(int)
        green_color = (0, 255, 0)
        cv2.circle(undistorted_img, tuple(point), 2, green_color, -1)
    

    cv2.imshow('Distorted Image', distorted_img)
    cv2.imshow('Undistorted Image', undistorted_img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
import cv2
import numpy as np
import math

class CameraPoseCalibration:
    
    def __init__(self):
        self.img = cv2.imread("../images/field.jpg")
        
        print "Please select red points in this order: left mid, left top, right top and bottom mid"        
        # marker points coordinate in world space
        self.marker_points_in_map = [[0, 1.2, 0], [0, 2.4, 0], [2.4, 2.4, 0], [1.2, 0, 0]]
        # marker points in image space, to be computed
        self.marker_points_in_image = []
        
        # default camera matrix and distortion coefficients for the kinect camera.
        self.camera_matrix = np.array([[525.0,   0.0, 319.5],
                                       [  0.0, 525.0, 239.5],
                                       [  0.0,   0.0,   1.0]])
        self.dist_coefs = np.array([[0.0, 0.0, 0.0, 0.0, 0.0]])        
        
        cv2.imshow("image", self.img)
        cv2.setMouseCallback("image", self.on_mouse)
        
    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.cv.CV_EVENT_LBUTTONDOWN:
            print "selected point (%i,%i)" % (x, y)
            self.marker_points_in_image.append([x, y])
            if len(self.marker_points_in_map) == len(self.marker_points_in_image):
                self.calibrate()
            
    def calibrate(self):
        print "calibrating..."
        
        # computing rotation and translation in camera space
        # for many points, use solvePnPRansac method!
        _, rvec, tvec = cv2.solvePnP(np.array(self.marker_points_in_map, dtype=np.float32),
                                     np.array(self.marker_points_in_image, dtype=np.float32).reshape(-1, 2),
                                     self.camera_matrix,
                                     self.dist_coefs)
        
        # draw a point on image to test whether the pose is correct.
        print "drawing a red circle in the mid"
        self.result_img = np.array(self.img)
        for point_in_world in [[1.2, 1.2, 0]]:
            point_im_image, _ = cv2.projectPoints(np.array([[point_in_world[0], point_in_world[1], point_in_world[2]]], dtype=np.float32),
                                                  rvec,
                                                  tvec,
                                                  self.camera_matrix,
                                                  self.dist_coefs)                                    
            cv2.circle(self.result_img, (int(point_im_image[0,0,0]), int(point_im_image[0,0,1])), 2, (0, 0, 255), -1)
        cv2.imshow("result", self.result_img)
        
        # show warped image
        w, h = 480, 480
        src_pts = np.array([[0, 0, 0], [0, 2.4, 0], [2.4, 2.4, 0], [2.4, 0, 0]], dtype=np.float32)
        projected_src_pts, _ = cv2.projectPoints(src_pts, rvec, tvec, self.camera_matrix, self.dist_coefs)        
        projected_src_pts = projected_src_pts.reshape((-1, 2))                
        dst_pts = np.array([[0, h-1], [0, 0], [w-1, 0], [w-1, h-1]], dtype=np.float32)
        warp_mat = cv2.getPerspectiveTransform(projected_src_pts, dst_pts)
        perspective_warped_img = cv2.warpPerspective(self.img, warp_mat, (w, h))
        cv2.imshow("warped", perspective_warped_img)
                
        # we need the pose in world space
        Rodrigues, _ = cv2.Rodrigues(rvec)
        T = euler_matrix(np.pi/2, -np.pi/2, 0)
        R = np.eye(4)
        R[:-1, :-1] = Rodrigues
        R[:-1, -1] = tvec.T
        R = np.linalg.inv(R)
        R = R.dot(T)
        
        rpy = euler_from_matrix(R)
        print "camera pose in world space:"
        print "    translation=(%f,%f,%f)" % (R[0,3], R[1,3], R[2,3])
        print "    rpy=(%f,%f,%f)" % (rpy[0], rpy[1], rpy[2])
                
        self.marker_points_in_image = []
    
    def start(self):
        while True:
            code = cv2.waitKey(30) & 0xFF
            if code in [27, ord('Q'), ord('q')]:
                break
            cv2.imshow("image", self.img)
        cv2.destroyAllWindows()
        
        

##############################################################################
# following rotation related methods are copied from ROS tf.transformations  #
##############################################################################

# epsilon for testing whether a number is close to zero
_EPS = np.finfo(float).eps * 4.0

# axis sequences for Euler angles
_NEXT_AXIS = [1, 2, 0, 1]

# map axes strings to/from tuples of inner axis, parity, repetition, frame
_AXES2TUPLE = {
    'sxyz': (0, 0, 0, 0), 'sxyx': (0, 0, 1, 0), 'sxzy': (0, 1, 0, 0),
    'sxzx': (0, 1, 1, 0), 'syzx': (1, 0, 0, 0), 'syzy': (1, 0, 1, 0),
    'syxz': (1, 1, 0, 0), 'syxy': (1, 1, 1, 0), 'szxy': (2, 0, 0, 0),
    'szxz': (2, 0, 1, 0), 'szyx': (2, 1, 0, 0), 'szyz': (2, 1, 1, 0),
    'rzyx': (0, 0, 0, 1), 'rxyx': (0, 0, 1, 1), 'ryzx': (0, 1, 0, 1),
    'rxzx': (0, 1, 1, 1), 'rxzy': (1, 0, 0, 1), 'ryzy': (1, 0, 1, 1),
    'rzxy': (1, 1, 0, 1), 'ryxy': (1, 1, 1, 1), 'ryxz': (2, 0, 0, 1),
    'rzxz': (2, 0, 1, 1), 'rxyz': (2, 1, 0, 1), 'rzyz': (2, 1, 1, 1)}

_TUPLE2AXES = dict((v, k) for k, v in _AXES2TUPLE.items())

def euler_matrix(ai, aj, ak, axes='sxyz'):
    """Return homogeneous rotation matrix from Euler angles and axis sequence.

    ai, aj, ak : Euler's roll, pitch and yaw angles
    axes : One of 24 axis sequences as string or encoded tuple

    >>> R = euler_matrix(1, 2, 3, 'syxz')
    >>> numpy.allclose(numpy.sum(R[0]), -1.34786452)
    True
    >>> R = euler_matrix(1, 2, 3, (0, 1, 0, 1))
    >>> numpy.allclose(numpy.sum(R[0]), -0.383436184)
    True
    >>> ai, aj, ak = (4.0*math.pi) * (numpy.random.random(3) - 0.5)
    >>> for axes in _AXES2TUPLE.keys():
    ...    R = euler_matrix(ai, aj, ak, axes)
    >>> for axes in _TUPLE2AXES.keys():
    ...    R = euler_matrix(ai, aj, ak, axes)

    """
    try:
        firstaxis, parity, repetition, frame = _AXES2TUPLE[axes]
    except (AttributeError, KeyError):
        _ = _TUPLE2AXES[axes]
        firstaxis, parity, repetition, frame = axes

    i = firstaxis
    j = _NEXT_AXIS[i+parity]
    k = _NEXT_AXIS[i-parity+1]

    if frame:
        ai, ak = ak, ai
    if parity:
        ai, aj, ak = -ai, -aj, -ak

    si, sj, sk = math.sin(ai), math.sin(aj), math.sin(ak)
    ci, cj, ck = math.cos(ai), math.cos(aj), math.cos(ak)
    cc, cs = ci*ck, ci*sk
    sc, ss = si*ck, si*sk

    M = np.identity(4)
    if repetition:
        M[i, i] = cj
        M[i, j] = sj*si
        M[i, k] = sj*ci
        M[j, i] = sj*sk
        M[j, j] = -cj*ss+cc
        M[j, k] = -cj*cs-sc
        M[k, i] = -sj*ck
        M[k, j] = cj*sc+cs
        M[k, k] = cj*cc-ss
    else:
        M[i, i] = cj*ck
        M[i, j] = sj*sc-cs
        M[i, k] = sj*cc+ss
        M[j, i] = cj*sk
        M[j, j] = sj*ss+cc
        M[j, k] = sj*cs-sc
        M[k, i] = -sj
        M[k, j] = cj*si
        M[k, k] = cj*ci
    return M

def euler_from_matrix(matrix, axes='sxyz'):
    """Return Euler angles from rotation matrix for specified axis sequence.

    axes : One of 24 axis sequences as string or encoded tuple

    Note that many Euler angle triplets can describe one matrix.

    >>> R0 = euler_matrix(1, 2, 3, 'syxz')
    >>> al, be, ga = euler_from_matrix(R0, 'syxz')
    >>> R1 = euler_matrix(al, be, ga, 'syxz')
    >>> numpy.allclose(R0, R1)
    True
    >>> angles = (4.0*math.pi) * (numpy.random.random(3) - 0.5)
    >>> for axes in _AXES2TUPLE.keys():
    ...    R0 = euler_matrix(axes=axes, *angles)
    ...    R1 = euler_matrix(axes=axes, *euler_from_matrix(R0, axes))
    ...    if not numpy.allclose(R0, R1): print axes, "failed"

    """
    try:
        firstaxis, parity, repetition, frame = _AXES2TUPLE[axes.lower()]
    except (AttributeError, KeyError):
        _ = _TUPLE2AXES[axes]
        firstaxis, parity, repetition, frame = axes

    i = firstaxis
    j = _NEXT_AXIS[i+parity]
    k = _NEXT_AXIS[i-parity+1]

    M = np.array(matrix, dtype=np.float64, copy=False)[:3, :3]
    if repetition:
        sy = math.sqrt(M[i, j]*M[i, j] + M[i, k]*M[i, k])
        if sy > _EPS:
            ax = math.atan2( M[i, j],  M[i, k])
            ay = math.atan2( sy,       M[i, i])
            az = math.atan2( M[j, i], -M[k, i])
        else:
            ax = math.atan2(-M[j, k],  M[j, j])
            ay = math.atan2( sy,       M[i, i])
            az = 0.0
    else:
        cy = math.sqrt(M[i, i]*M[i, i] + M[j, i]*M[j, i])
        if cy > _EPS:
            ax = math.atan2( M[k, j],  M[k, k])
            ay = math.atan2(-M[k, i],  cy)
            az = math.atan2( M[j, i],  M[i, i])
        else:
            ax = math.atan2(-M[j, k],  M[j, j])
            ay = math.atan2(-M[k, i],  cy)
            az = 0.0

    if parity:
        ax, ay, az = -ax, -ay, -az
    if frame:
        ax, az = az, ax
    return ax, ay, az

if __name__ == '__main__':
    CameraPoseCalibration().start()
    
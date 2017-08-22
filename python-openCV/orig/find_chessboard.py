import cv2
import numpy as np

def find_chessboard(img, square_size=0.05, pattern_size=(9, 6)):
    result_img = np.array(img)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    
    found, corners = cv2.findChessboardCorners(gray_img, pattern_size)
    if found:
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
        cv2.cornerSubPix(gray_img, corners, (4, 4), (-1, -1), term)
        cv2.drawChessboardCorners(result_img, pattern_size, corners, found)
        
    return found, result_img, pattern_points, corners.reshape(-1, 2)
    

if __name__ == '__main__':
    img = cv2.imread("../images/chessboard2.jpg")
    found, result_img, pattern_points, corner_points = find_chessboard(img, square_size=0.05, pattern_size=(9, 6))    
    cv2.imshow("Chessboard", result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
__author__ = 'Aravinth Panchadcharam'
__email__ = "me@aravinth.info"
__date__ = '22/04/15'

import cv2

if __name__ == '__main__':
    img = cv2.imread('test.jpg', 0)
    image_small = cv2.resize(img, (800, 600))
    cv2.imshow('image', image_small)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#!/usr/bin/env python
"""
Test cases for MySky
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('MySkyHome.png', 0)
img2 = img.copy()
template = cv2.imread('Border.jpg', 0)
mask = cv2.imread('Mask.png', 0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', \
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    count = 0
    while count < 5:
        res = cv2.matchTemplate(img, template, method, mask)

        if res == None:
            break

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
            bottom_right = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
        else:
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

        print_image = img.copy()
        cv2.rectangle(print_image, top_left, bottom_right, 255, 2)

        plt.subplot(121), plt.imshow(res, cmap='gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(print_image, cmap='gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()

        # Hide match under black rectangle:
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), -1)
        count += 1

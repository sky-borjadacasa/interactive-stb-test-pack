#!/usr/bin/env python
"""
Library with utilities for navigating SkyPlusHD box menus
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

# Constants:
TM_CCOEFF_THRESHOLD = 100000000 # Maybe it should be 50000000
TM_CCOEFF_NORMED_THRESHOLD = 0.8

# Image files:
IMAGE_BORDER = 'images/Border.png'
IMAGE_BORDER_SMALL = 'images/BorderSmall.png'
IMAGE_MASK = 'images/Mask.png'
IMAGE_MASK_SMALL = 'images/MaskSmall.png'

# Test image files:
TEST_IMAGE_MYSKY_HOME = 'MySkyHome.png'
TEST_IMAGE_MYSKY_MENU = 'MySkyMenu.png'
TEST_IMAGE_MYSKY_MENU_1 = 'MySkyMenu1.png'


class MySkyMenuItem:
    """Class to store the attributes of a MySky menu item"""

    _text = ''

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        # TODO: Get text from box

    def menu_text(self):
        return self._text





# XXX - Testing code

img = cv2.imread(TEST_IMAGE_MYSKY_MENU, 0)
img2 = img.copy()
template = cv2.imread(IMAGE_BORDER, 0)
mask = cv2.imread(IMAGE_MASK, 0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', \
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
methods = ['cv2.TM_CCOEFF']

menu_items = []

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    count = 0
    threshold = 100000000
    threshold = 50000000
    while count < 15:
        count += 1
        res = cv2.matchTemplate(img, template, method, mask)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print '{0}, {1}'.format(min_val, max_val)
        if max_val < threshold:
            continue

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
            bottom_right = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            item = MySkyMenuItem(top_left, bottom_right)
            menu_items.append(item)
        else:
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            item = MySkyMenuItem(top_left, bottom_right)
            menu_items.append(item)

        # Hide match under black rectangle:
        cv2.rectangle(img, item.top_left, item.bottom_right, (0, 0, 0), -1)

# Show all menus found:
print_image = img2.copy()
menu_items.sort(key=lambda x: x.top_left[1])

for item in menu_items:
    print 'Item: ({0}, {1}) -> {2}'.format(item.top_left, item.bottom_right, item.top_left[1])
    cv2.rectangle(print_image, item.top_left, item.bottom_right, 255, 2)

plt.subplot(121), plt.imshow(res, cmap='gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(print_image, cmap='gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle(meth)

plt.show()

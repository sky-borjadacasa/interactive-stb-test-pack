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
MAX_MATCHING_LOOPS = 15

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

original_image = cv2.imread(TEST_IMAGE_MYSKY_HOME, 0)
template = cv2.imread(IMAGE_BORDER, 0)
mask = cv2.imread(IMAGE_MASK, 0)
w, h = template.shape[::-1]

# These are the 6 methods for comparison in a list:
# cv2.TM_CCOEFF
# cv2.TM_CCOEFF_NORMED
# cv2.TM_CCORR
# cv2.TM_CCORR_NORMED
# cv2.TM_SQDIFF
# cv2.TM_SQDIFF_NORMED


method = cv2.TM_CCOEFF
img = original_image.copy()
menu_items = []

# Apply template Matching
count = 0
while count < MAX_MATCHING_LOOPS:
    count += 1
    res = cv2.matchTemplate(img, template, method, mask)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print '{0}, {1}'.format(min_val, max_val)
    if max_val < TM_CCOEFF_THRESHOLD:
        continue

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    item = MySkyMenuItem(top_left, bottom_right)
    menu_items.append(item)

    # Hide match under black rectangle:
    cv2.rectangle(img, item.top_left, item.bottom_right, (0, 0, 0), -1)

# Show all menus found:
print_image = original_image.copy()
menu_items.sort(key=lambda x: x.top_left[1])

for item in menu_items:
    print 'Item: ({0}, {1}) -> {2}'.format(item.top_left, item.bottom_right, item.top_left[1])
    cv2.rectangle(print_image, item.top_left, item.bottom_right, 255, 2)

plt.subplot(121), plt.imshow(res, cmap='gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(print_image, cmap='gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle('Method: TM_CCOEFF')

plt.show()

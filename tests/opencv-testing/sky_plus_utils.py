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
MY_SKY_REGION = ((880, 0), (1280 - 1, 720 - 1)) # The 400 pixels to the right and the whole height of the screen

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

def find_image_menu_items(original_image, template, template_mask=None, region=None, show_results=False):
    """Function to find the menu items in a given image.
    This function will return only menu elements with images on them ordered by vertical position.

    Args:
        image (numpy.ndarray): The image to analyse
        template (numpy.ndarray): Template of the menu item
        template (numpy.ndarray): Mask to apply of the menu item
        region (tuple(tuple(int))): Region of the image to search defined by the top-left and bottom-right coordinates

    Returns:
        List of the menu items found
    """

    # These are the 6 methods for comparison in a list:
    # cv2.TM_CCOEFF
    # cv2.TM_CCOEFF_NORMED
    # cv2.TM_CCORR
    # cv2.TM_CCORR_NORMED
    # cv2.TM_SQDIFF
    # cv2.TM_SQDIFF_NORMED
    method = cv2.TM_CCOEFF
    width, height = template.shape[::-1]
    
    if region is not None:
        x1 = region[0][0]
        x2 = region[1][0]
        y1 = region[0][1]
        y2 = region[1][1]
        image = original_image[y1:y2, x1:x2].copy()
    else:
        image = original_image.copy()
    menu_items = []

    # Apply template Matching
    count = 0
    while count < MAX_MATCHING_LOOPS:
        count += 1
        res = cv2.matchTemplate(image, template, method, template_mask)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < TM_CCOEFF_THRESHOLD:
            print '{0} < {1}'.format(max_val, TM_CCOEFF_THRESHOLD)
            continue
        else:
            print '{0} > {1}'.format(max_val, TM_CCOEFF_THRESHOLD)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        top_left = max_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)

        # Hide match under black rectangle:
        cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), -1)

        if region is not None:
            top_left = (top_left[0] + x1, top_left[1] + y1)
            bottom_right = (bottom_right[0] + x1, bottom_right[1] + y1)
        item = MySkyMenuItem(top_left, bottom_right)
        menu_items.append(item)

    menu_items.sort(key=lambda x: x.top_left[1])
    
    if show_results:
        plot_results(original_image, res, menu_items)

    return menu_items

def plot_results(image, matching_result, menu_items, region=None):
    """Function to plot the menus found in an image.

    Args:
        image (numpy.ndarray): The image analysed
        matching_result (numpy.ndarray): The result of the analysis
        menu_items (list(MySkyMenuItem)): List of menu items found
        region (tuple(tuple(int))): Region of the image analysed defined by the top-left and bottom-right coordinates
    """
    print_image = image.copy()

    # TODO: Print region
    # TODO: Remove res?

    count = 0
    for item in menu_items:
        print 'Item {0}: ({1}, {2})'.format(count, item.top_left, item.bottom_right)
        cv2.rectangle(print_image, item.top_left, item.bottom_right, 255, 2)
        count += 1

    plt.subplot(121), plt.imshow(matching_result, cmap='gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(print_image, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle('Method: TM_CCOEFF')

    plt.show()



# XXX - Testing code

image = cv2.imread(TEST_IMAGE_MYSKY_HOME, 0)
template = cv2.imread(IMAGE_BORDER, 0)
mask = cv2.imread(IMAGE_MASK, 0)

menu_items = find_image_menu_items(image, template, mask, region=MY_SKY_REGION, show_results=True)

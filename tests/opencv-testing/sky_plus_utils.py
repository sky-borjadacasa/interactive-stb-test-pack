#!/usr/bin/env python
"""
Library with utilities for navigating SkyPlusHD box menus
"""

import cv2
import numpy as np
import tesserocr
from PIL import Image
from matplotlib import pyplot as plt

# Constants:
TM_CCOEFF_THRESHOLD = 50000000
TM_CCOEFF_NORMED_THRESHOLD = 0.8
MAX_MATCHING_LOOPS = 15
MY_SKY_REGION = ((880, 0), (1280 - 1, 720 - 1)) # The 400 pixels to the right and the whole height of the screen
MY_SKY_TEXT_MENU_REGION = ((920, 125), (1240, 550))
VERTICAL_UNSELECTED_TEXT_MENU_ITEM_SIZE = 50

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

    text = ''

    def __init__(self, image, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.text = find_text(image, (top_left, bottom_right))

    def region(self):
        return (self.top_left, self.bottom_right)

def generic_item_find(original_image, template, template_mask=None, region=None):
    """Function to find the menu items matching a given template.
    This function will return only menu elements with images on them ordered by vertical position.

    Args:
        image (numpy.ndarray): The image to analyse
        template (numpy.ndarray): Template of the menu item
        template_mask (numpy.ndarray): Mask to apply of the menu item
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
    while True:
        count += 1
        res = cv2.matchTemplate(image, template, method, template_mask)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < TM_CCOEFF_THRESHOLD:
            print '{0} < {1}'.format(max_val, TM_CCOEFF_THRESHOLD)
            break
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
        item = MySkyMenuItem(original_image, top_left, bottom_right)
        menu_items.append(item)

    menu_items.sort(key=lambda x: x.top_left[1])
    return menu_items

def find_image_menu_items(original_image, show_results=False):
    """Function to find the menu items with an image in a given image.
    This function will return only menu elements with images on them ordered by vertical position.

    Args:
        image (numpy.ndarray): The image to analyse
        show_results (bool): If True, will open a window with the items found drawn on top of the original image

    Returns:
        List of the menu items found
    """

    template = cv2.imread(IMAGE_BORDER, 0)
    mask = cv2.imread(IMAGE_MASK, 0)
    menu_items = generic_item_find(original_image, template, mask, region=MY_SKY_REGION)
    
    if show_results:
        plot_results(original_image, menu_items, region=MY_SKY_REGION)

    return menu_items

def find_text_menu_items(original_image, show_results=False):
    """Function to find the menu items with only text in a given image.
    This function will return only menu elements with text on them ordered by vertical position.

    Args:
        image (numpy.ndarray): The image to analyse
        show_results (bool): If True, will open a window with the items found drawn on top of the original image

    Returns:
        List of the menu items found
    """

    # This will find the only selected menu item:
    template = cv2.imread(IMAGE_BORDER_SMALL, 0)
    mask = cv2.imread(IMAGE_MASK_SMALL, 0)
    menu_items = generic_item_find(original_image, template, mask, region=MY_SKY_REGION)

    # Try to find not selected items, based on size and OCR results (later)
    selected_item = menu_items[0]
    region_top = MY_SKY_TEXT_MENU_REGION[0][1]
    region_bottom = MY_SKY_TEXT_MENU_REGION[1][1]

    # Search up:
    point = selected_item.top_left[1]
    while point >= region_top:
        print 'Top: {0}, Point: {1}'.format(region_top, point)
        point -= VERTICAL_UNSELECTED_TEXT_MENU_ITEM_SIZE
        if point >= region_top:
            top_left = (selected_item.top_left[0], point)
            bottom_right = (selected_item.bottom_right[0], point + VERTICAL_UNSELECTED_TEXT_MENU_ITEM_SIZE)
            item = MySkyMenuItem(original_image, top_left, bottom_right)
            menu_items.append(item)
        else:
            break

    # Search down:
    point = menu_items[0].bottom_right[1]
    while point <= region_bottom:
        print 'Bottom: {0}, Point: {1}'.format(region_bottom, point)
        if point + VERTICAL_UNSELECTED_TEXT_MENU_ITEM_SIZE  <= region_bottom:
            top_left = (selected_item.top_left[0], point)
            bottom_right = (selected_item.bottom_right[0], point + VERTICAL_UNSELECTED_TEXT_MENU_ITEM_SIZE)
            item = MySkyMenuItem(original_image, top_left, bottom_right)
            menu_items.append(item)
        else:
            break
        point += VERTICAL_UNSELECTED_TEXT_MENU_ITEM_SIZE

    for item in menu_items:
        item.text = find_text(original_image, item.region())

    # Clean and sort results:
    menu_items = [item for item in menu_items if item.text]
    menu_items.sort(key=lambda x: x.top_left[1])

    if show_results:
        plot_results(original_image, menu_items, region=MY_SKY_TEXT_MENU_REGION)

    return menu_items


def plot_results(image, menu_items, region=None):
    """Function to plot the menus found in an image.

    Args:
        image (numpy.ndarray): The image analysed
        menu_items (list(MySkyMenuItem)): List of menu items found
        region (tuple(tuple(int))): Region of the image analysed defined by the top-left and bottom-right coordinates
    """
    print_image = image.copy()

    if region is not None:
        cv2.rectangle(print_image, region[0], region[1], 255, 2)

    count = 0
    for item in menu_items:
        print 'Item {0}: ({1}, {2})'.format(count, item.top_left, item.bottom_right)
        cv2.rectangle(print_image, item.top_left, item.bottom_right, 255, 2)
        count += 1

    show_numpy_image(print_image, 'Detected Point', 'Method: TM_CCOEFF')

def find_text(image, region):
    cropped_image = crop_image(image, region)
    pil_image = Image.fromarray(np.rollaxis(cropped_image, 0, 1))
    return tesserocr.image_to_text(pil_image).strip()

def crop_image(image, region):
    x1 = region[0][0]
    x2 = region[1][0]
    y1 = region[0][1]
    y2 = region[1][1]
    return image[y1:y2, x1:x2].copy()

def show_pillow_image(image, region):
    cropped_image = crop_image(image, region)
    pil_image = Image.fromarray(np.rollaxis(cropped_image, 0, 1))
    pil_image.show()

def show_numpy_image(image, title, subtitle):
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.suptitle(subtitle)
    plt.xticks([])
    plt.yticks([])
    plt.show()






# XXX - Testing code

image = cv2.imread(TEST_IMAGE_MYSKY_HOME, 0)
menu_items = find_image_menu_items(image, show_results=True)

image = cv2.imread(TEST_IMAGE_MYSKY_MENU, 0)
menu_items = find_image_menu_items(image, show_results=True)

image = cv2.imread(TEST_IMAGE_MYSKY_MENU_1, 0)
menu_items = find_text_menu_items(image, show_results=True)

for item in menu_items:
    print 'Item: {0}, ({1})'.format(item.text, item.region())
    show_pillow_image(image, item.region())

print 'Finish'

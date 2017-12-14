#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Library with utilities for navigating SkyPlusHD box menus
"""

import time
import mysky_constants
import cv2
import numpy as np
from scipy.stats import itemfreq
from fuzzywuzzy import process
import stbt

DEBUG_MODE = True
IMAGE_DEBUG_MODE = False

def debug(text):
    """Print the given text if debug mode is on.

    Args:
        text (str): The text to print
    """
    if DEBUG_MODE:
        print '[DEBUG] {0}'.format(text)

def crop_image(image, region):
    """Crop the image

    Args:
        image (numpy.ndarray): Image to crop
        region (stbt.Region): Region to crop

    Returns:
        Cropped image
    """
    if region is None:
        return image.copy()
    return image[region.y:region.bottom, region.x:region.right].copy()

def rgb_luminance(color):
    """Calculate luminance of RGB color

    Args:
        color (numpy.ndarray): Color to search in RGB format

    Returns:
        Luminance of the color
    """
    return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]

def bgr_to_rgb(color):
    """Convert color from BGR to RGB

    Args:
        color_a (numpy.ndarray): Color in BGR format

    Returns:
        Color in RGB format
    """
    return color[::-1]

def color_distance(color_a, color_b):
    """Tell if two colors are close

    Args:
        color_a (numpy.ndarray): First color in RGB format
        color_b (numpy.ndarray): Second color in RGB format

    Returns:
        Color distance between the two colors
    """
    r_distance = abs(color_a[0] - color_b[0])
    g_distance = abs(color_a[1] - color_b[1])
    b_distance = abs(color_a[2] - color_b[2])
    return r_distance + g_distance + b_distance

def is_similar_color_rgb(color_a, color_b):
    """Tell if two colors are similar

    Args:
        color_a (numpy.ndarray): First color in RGB format
        color_b (numpy.ndarray): Second color in RGB format

    Returns:
        True if colors distance is lower than defined threshold
    """
    difference = abs(rgb_luminance(color_a) - rgb_luminance(color_b))
    distance = color_distance(color_a, color_b)
    return difference < mysky_constants.COLOR_LUMINANCE_THRESHOLD and distance < mysky_constants.COLOR_DISTANCE_THRESHOLD

def get_palette(image, region):
    """Get the dominant colors of a region

    Args:
        image (numpy.ndarray): Image to search
        region (stbt.Region): Region of the image to search

    Returns:
        Palette of colors
        Color frequency of image
    """
    cropped_image = crop_image(image, region)
    arr = np.float32(cropped_image)
    pixels = arr.reshape((-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centroids = cv2.kmeans(pixels, K=mysky_constants.PALETTE_SIZE, bestLabels=None, criteria=criteria, attempts=10, flags=flags)

    palette = np.uint8(centroids)
    color_frequency = itemfreq(labels)
    color_frequency.sort(0)

    return palette, color_frequency

def is_color_in_palette(palette, color_frequency, color_to_find):
    """Find the most common color in a palette that matches the wanted color

    Args:
        palette (numpy.ndarray): Palette of colors
        color_frequency (numpy.ndarray): Color frequency of image
        color_to_find (tuple(int)): Color to find

    Returns:
        True if if the color is in the palete
    """
    for label in color_frequency[::-1]:
        color = palette[label[0]]
        rgb_color = bgr_to_rgb(color)
        if is_similar_color_rgb(rgb_color, color_to_find):
            return True
    return False

def press_digits(digits):
    """Press a sequence of digits

    Args:
        digits (string): digits to input
    """
    for digit in digits:
        button = 'KEY_{0}'.format(digit)
        stbt.press(button)

def go_to_channel(channel):
    """Got to the given channel

    Args:
        channel (string): Channel to input
    """
    assert len(channel) == 3
    press_digits(channel)

def open_secret_scene():
    """Open secret scene menu
    """
    press_digits('062840')

class SkyPlusTestUtils(object):
    """Class that contains the logic to analyse the contents of the MySky menu"""

    def __init__(self, image):
        self.fuzzy_set = mysky_constants.load_fuzzy_set()
        self.image = image

    def find_text(self, region, fuzzy=True, char_whitelist=mysky_constants.OCR_CHAR_WHITELIST):
        """Read the text in the given region

        Args:
            region (stbt.Region): Region of the image to search defined by the top-left and bottom-right coordinates

        Returns:
            Text of the given item
        """
        cropped_image = crop_image(self.image, region)
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        text = ''
        ocr_options = {'tessedit_char_whitelist': char_whitelist}
        text = stbt.ocr(region=region, tesseract_config=ocr_options).strip().encode('utf-8')
        debug('Text found: [{0}] in region {1}'.format(text, region))
        if text and fuzzy:
            text = self.fuzzy_match(text)
        debug('Text matched: [{0}] in region {1}'.format(text, region))
        # Debugging:
        if IMAGE_DEBUG_MODE:
            cv2.imwrite('finding_text_{0}.jpg'.format(time.time()), crop_image(self.image, region))

        return text

    def match_color(self, region, color):
        """Tell if the region dominant color matches (aprox.) the given color

        Args:
            region (stbt.Region): Region of the image to search defined by the top-left and bottom-right coordinates
            color (numpy.ndarray): Color to match in RGB format

        Returns:
            True if if the dominant color matches the given color
        """
        palette, color_frequency = get_palette(self.image, region)
        debug('Palette: {0}'.format(palette))
        debug('Color frequency: {0}'.format(color_frequency))
        selected = is_color_in_palette(palette, color_frequency, color)

        # Debugging:
        if IMAGE_DEBUG_MODE:
            cv2.imwrite('matching_color_{0}.jpg'.format(time.time()), crop_image(self.image, region))

        debug('Color matched: {0}, {1}'.format(selected, color))

        return selected


    def fuzzy_match(self, text):
        """Get the text fuzzy matched against our dictionary

        Args:
            text (str): Text to match

        Returns:
            Matched text
        """
        matches = process.extract(text, self.fuzzy_set, limit=3)
        debug('Matches for "{0}":\n{1}'.format(text, matches))
        # We get directly the most likely match
        return matches[0][0]

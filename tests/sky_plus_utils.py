#!/usr/bin/env python
"""
Library with utilities for navigating SkyPlusHD box menus
"""

import string
import cv2
import numpy as np
from scipy.stats import itemfreq
from fuzzywuzzy import process

# Try to import testing libs:
try:
    from PIL import Image
    from matplotlib import pyplot as plt
except ImportError:
    print 'Couldn\'t import testing libs'

# Switch between tesserocr for testing and stbt.ocr for running in the tester:
useStbtOcr = False
try:
    import stbt
    from stbt import Region
    useStbtOcr = True
except ImportError:
    import tesserocr

# Constants:

# Text recognition:
OCR_CHAR_WHITELIST = string.ascii_letters + ' ' + string.digits

# Colors:
YELLOW_BACKGROUND_RGB = np.array([235, 189, 0])
BLUE_BACKGROUND_RGB = np.array([30, 87, 161])
BLACK_RGB = np.array([0, 0, 0])
WHITE_RGB = np.array([255, 255, 255])
COLOR_THRESHOLD = 10
PALETTE_SIZE = 2

class MySkyMenuItem(object):
    """Class to store the attributes of a MySky menu item"""

    text = ''
    selected = False
    region = None

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.region = (top_left, bottom_right)

def load_fuzzy_set():
    """Function to load the fuzzy matching expression dictionary

    Returns:
        List of the expressions to match
    """
    lines = ['Sky Q', \
        'Manage your account', \
        'Fix a problem', \
        'Bills and payments', \
        'TV package and settings', \
        'Broadband and Talk', \
        'My details and messages', \
        'TV picture problems', \
        'No satelite signal', \
        'Forgotten PIN', \
        'Good Morning', \
        'Good Afternoon',
        'Find out more',
        'Loading...']
    return lines

def crop_image(image, region):
    """Crop the image

    Args:
        image (numpy.ndarray): Image to crop
        region (tuple(tuple(int))): Region to crop

    Returns:
        Cropped image
    """
    if region is None:
        return image.copy()
    x1 = region[0][0]
    x2 = region[1][0]
    y1 = region[0][1]
    y2 = region[1][1]
    return image[y1:y2, x1:x2].copy()

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

def is_similar_color_rgb(color_a, color_b):
    """Tell if two colors are similar

    Args:
        color_a (numpy.ndarray): Color to search in RGB format
        color_b (numpy.ndarray): Color to search in RGB format

    Returns:
        True if colors distance is lower than defined threshold
    """
    distance = abs(rgb_luminance(color_a) - rgb_luminance(color_b))
    return distance < COLOR_THRESHOLD

def get_palette(image, region):
    """Get the dominant colors of a region

    Args:
        image (numpy.ndarray): Image to search
        region (tuple(tuple(int))): Region of the image to search

    Returns:
        Palette of colors
        Color frequency of image
    """
    cropped_image = crop_image(image, region)
    arr = np.float32(cropped_image)
    pixels = arr.reshape((-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centroids = cv2.kmeans(pixels, K=PALETTE_SIZE, bestLabels=None, criteria=criteria, attempts=10, flags=flags)

    palette = np.uint8(centroids)
    color_frequency = itemfreq(labels)
    color_frequency.sort(0)

    return palette, color_frequency

def dominant_color(image, region, exclude_list=[]):
    """Get the dominant color of a region

    Args:
        image (numpy.ndarray): Image to search
        region (tuple(tuple(int))): Region of the image to search
        exclude_list (list): List of colors to avoid searching for
        include_list (list): List of colors to search for

    Returns:
        RGB color found
    """
    palette, color_frequency = get_palette(image, region)

    for label in color_frequency[::-1]:
        color = palette[label[0]]
        rgb_color = bgr_to_rgb(color)
        exclude = False
        for exclude_color in exclude_list:
            if is_similar_color_rgb(rgb_color, exclude_color):
                exclude = True
                break
        if exclude:
            continue
        else:
            return color

def is_color_in_palette(palette, color_frequency, color_to_find):
    """Find the most common color in a palette that matches the wanted color

    Args:
        palette (numpy.ndarray): Palette of colors
        color_frequency (numpy.ndarray): Color frequency of image
        color_to_find (tuple(int)): Region of the image to search

    Returns:
        The most common color in a palette that matches the wanted color
    """
    for label in color_frequency[::-1]:
        color = palette[label[0]]
        rgb_color = bgr_to_rgb(color)
        if is_similar_color_rgb(rgb_color, color_to_find):
            return True
    return False

def get_stbt_region(region):
    """Convert a region in ((x1, y1), (x2, y2)) format to a stbt.Region type

    Args:
        region (tuple(tuple(int))): Region to convert

    Returns:
        stbt.Region object representing the same area
    """
    stbt_region = Region(region[0][0], region[0][1], right=region[1][0], bottom=region[1][1])
    return stbt_region

def get_utils_region(stbt_region):
    """Convert a stbt.Region type to a region in ((x1, y1), (x2, y2)) format 

    Args:
        stbt.Region object representing the same area to convert

    Returns:
        Region in the (tuple(tuple(int))) format
    """
    region = ((stbt_region.x, stbt_region.y), (stbt_region.right, stbt_region.bottom))
    stbt_region = Region(region[0][0], region[0][1], right=region[1][0], bottom=region[1][1])
    return region

class SkyPlusTestUtils(object):
    """Class that contains the logic to analyse the contents of the MySky menu"""

    def __init__(self, image, debug_mode=False, show_images_results=False):
        self.coiso = 'cena'
        self.fuzzy_set = load_fuzzy_set()
        self.image = image
        self.debug_mode = debug_mode
        self.show_images_results = show_images_results

    def debug(self, text):
        """Print the given text if debug mode is on.

        Args:
            text (str): The text to print
        """
        if self.debug_mode:
            print text

    def find_text_in_box(self, region):
        """Read the text in the given region

        Args:
            region (tuple(tuple(int))): Region of the image to search defined by the top-left and bottom-right coordinates

        Returns:
            Text of the given item
        """
        cropped_image = crop_image(self.image, region)
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        text = ''
        if useStbtOcr:
            ocr_options = {'tessedit_char_whitelist': OCR_CHAR_WHITELIST}
            text = stbt.ocr(region=get_stbt_region(region), tesseract_config=ocr_options).strip().encode('utf-8')
            # XXX
            print 'Text found: [{0}] in region {1}'.format(text, region)
            if text:
                text = self.fuzzy_match(text)
            # XXX
            print 'Text matched: [{0}] in region {1}'.format(text, region)
        else:
            pil_image = Image.fromarray(np.rollaxis(cropped_image, 0, 1))
            if self.debug_mode and self.show_images_results:
                pil_image.show()

            with tesserocr.PyTessBaseAPI() as api:
                api.SetImage(pil_image)
                api.SetVariable('tessedit_char_whitelist', OCR_CHAR_WHITELIST)
                text = api.GetUTF8Text().strip().encode('utf-8')
                if text:
                    text = self.fuzzy_match(text)

        # Find out if selected or not:
        palette, color_frequency = get_palette(self.image, region)
        print 'Palette: {0}'.format(palette)
        print 'Color frequency: {0}'.format(color_frequency)
        selected = is_color_in_palette(palette, color_frequency, YELLOW_BACKGROUND_RGB)

        self.debug('Found text: {0}, {1}'.format(text, selected))

        return text, selected

    def fuzzy_match(self, text):
        """Get the text fuzzy matched against our dictionary

        Args:
            text (str): Text to match

        Returns:
            Matched text
        """
        #matches = self.fuzzy_set.get(text)
        matches = process.extract(text, self.fuzzy_set, limit=3)
        self.debug('Matches for "{0}":\n{1}'.format(text, matches))
        # We get directly the most likely match
        return matches[0][0]

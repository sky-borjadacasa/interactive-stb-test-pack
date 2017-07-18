#!/usr/bin/env python
"""
Test cases for MySky
"""
# Import util:
def install_and_import(package, package_name=None):
    """Function to install and import the needed packages.

    Args:
        pacakge (str): The name of the package to import
        package_name (str): Name of the pip package when it's not the same as the package name
    """
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        if package_name is not None:
            pip.main(['install', package_name])
        else:
            pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

import os
import importlib
import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region
from time import sleep

os.system('sudo apt-get -y install python-scipy')
install_and_import('scipy.stats', 'scipy')
from scipy.stats import itemfreq
install_and_import('numpy')
import numpy as np

class MySkyMainMenu(FrameObject):

    @property
    def is_visible(self):
        return stbt.match('images/SkyTopLogo.png', region=MY_SKY_REGION)

    @property
    def message(self):
        return 'message'

    @property
    def _info(self):
        return match('images/SkyTopLogo.png', frame=self._frame)

# Constants:
TEST_IMAGE_MYSKY_HOME = 'screenshots/MySkyHomeOld.png'
YELLOW_BACKGROUND_RGB = np.array([235, 189, 0])
COLOR_THRESHOLD = 10
PALETTE_SIZE = 2

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

def is_yellow(image, region):
    # Find out if yellow or not:
    palette, color_frequency = get_palette(image, region)
    cropped_image = crop_image(image, region)
    print 'Image shape: {0}'.format(cropped_image.shape)
    print 'IMAGE ### {0} ###'.format(cropped_image)
    print 'Palette: {0}'.format(palette)
    print 'Color frequency: {0}'.format(color_frequency)
    yellow = is_color_in_palette(palette, color_frequency, YELLOW_BACKGROUND_RGB)

    print 'Is yellow: {0}'.format(yellow)

    return yellow

def test_get_yellow():
    """Open MySky app"""
    stbt.press('KEY_YELLOW')
    menu = stbt.wait_until(MySkyMainMenu)
    assert menu.is_visible
    print 'MySky menu is visible'
    
    sleep(10)

    testing_image = menu.frame
    region = ((960, 250), (964, 254))
    yellow = is_yellow(testing_image, region)

    return 0

#!/usr/bin/env python
"""
Library with utilities for navigating SkyPlusHD box menus
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

import importlib
import string
install_and_import('cv2', 'opencv-python')
install_and_import('numpy')
install_and_import('tesserocr')
install_and_import('PIL', 'pillow')
install_and_import('matplotlib')
install_and_import('scipy.stats', 'scipy')
install_and_import('fuzzyset')
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from scipy.stats import itemfreq
from fuzzyset import FuzzySet

# Constants:
TM_CCOEFF_THRESHOLD_BOX_ITEM = 250000000
TM_CCOEFF_THRESHOLD_TEXT_ITEM = 140000000
VERTICAL_TEXT_SIZE = 50
VERTICAL_TEXT_SIZE_WITH_IMAGE = 45
HORIZONAL_TEXT_MARGIN = 10

# Regions:
MY_SKY_REGION = ((880, 0), (1280 - 1, 720 - 1)) # The 400 pixels to the right and the whole height of the screen
MY_SKY_TEXT_MENU_REGION = ((920, 125), (1240, 550))

# Text recognition:
OCR_CHAR_WHITELIST = string.ascii_letters + ' ' + string.digits
FUZZY_DICT_FILENAME = 'fuzzy_dict.txt'

# Colors:
YELLOW_BACKGROUND_RGB = np.array([235, 189, 0])
BLUE_BACKGROUND_RGB = np.array([30, 87, 161])
BLACK_RGB = np.array([0, 0, 0])
WHITE_RGB = np.array([255, 255, 255])
COLOR_THRESHOLD = 10

# Image files:
IMAGE_BORDER = 'images/Border.png'
IMAGE_BORDER_BIG = 'images/BorderBig.png'
IMAGE_BORDER_SMALL = 'images/BorderSmall.png'
IMAGE_MASK = 'images/Mask.png'
IMAGE_MASK_BIG = 'images/MaskBig.png'
IMAGE_MASK_SMALL = 'images/MaskSmall.png'

# Test image files:
TEST_IMAGE_MYSKY_HOME = 'MySkyHome.png'
TEST_IMAGE_MYSKY_MENU = 'MySkyMenu.png'
TEST_IMAGE_MYSKY_MENU_1 = 'MySkyMenu1.png'

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
    dict_file = open(FUZZY_DICT_FILENAME, 'r')
    lines = [line.lstrip() for line in dict_file.read().split('\n')]
    return FuzzySet(lines)

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

def show_numpy_image(image, title, subtitle, convert=None):
    """Show the given image region on the screen

    Args:
        image (numpy.ndarray): Image to show
        title (str): Title to show
        subtitle (str): Subtitle to show
    """
    rgb_image = image
    if convert is not None:
        rgb_image = cv2.cvtColor(image, convert)
    plt.imshow(rgb_image, cmap='gray')
    plt.title(title)
    plt.suptitle(subtitle)
    plt.xticks([])
    plt.yticks([])
    plt.show()

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

def dominant_color(image, region, exclude_list=[]):
    """Get the dominant color of a region

    Args:
        image (numpy.ndarray): Image to search
        region (tuple(tuple(int))): Region of the image to search
        exclude_list (list): List of colors to avoid searching for

    Returns:
        RGB color found
    """
    cropped_image = crop_image(image, region)
    arr = np.float32(cropped_image)
    pixels = arr.reshape((-1, 3))

    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)

    palette = np.uint8(centroids)
    label_frequency = itemfreq(labels)
    label_frequency.sort(0)

    for label in label_frequency[::-1]:
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

# TODO - Clean
def intersection(a, b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0] + a[2], b[0] + b[2]) - x
    h = min(a[1] + a[3], b[1] + b[3]) - y
    if w < 0 or h < 0:
        return None
    return (x, y, w, h)

# TODO - Clean
def is_inside(a, b):
    # is b inside a?
    x_distance = a[0] - b[0]
    y_distance = a[1] - b[1]
    w_distance = a[0] + a[2] - b[0] - b[2]
    h_distance = a[1] + a[3] - b[1] - b[3]
    return x_distance <= 0 and y_distance <= 0 \
        and w_distance >= 0 and h_distance >= 0

# TODO - Clean
def boxes_are_similar(a, b):
    size_threshold = 30 # TODO: Fine tune
    x_distance = abs(a[0] - b[0])
    y_distance = abs(a[1] - b[1])
    w_distance = abs(a[0] + a[2] - b[0] - b[2])
    h_distance = abs(a[1] + a[3] - b[1] - b[3])
    return x_distance < size_threshold and y_distance < size_threshold \
        and w_distance < size_threshold and h_distance < size_threshold

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

    def generic_item_find(self, template, threshold, template_mask=None, region=None):
        """Function to find the menu items matching a given template.
        This function will return only menu elements with images on them ordered by vertical position.

        Args:
            template (numpy.ndarray): Template of the menu item
            threshold (int): The threshold to use for matching the template
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
        depth, width, height = template.shape[::-1]

        if region:
            x1 = region[0][0]
            x2 = region[1][0]
            y1 = region[0][1]
            y2 = region[1][1]
            image = self.image[y1:y2, x1:x2].copy()
        else:
            image = self.image.copy()
        menu_items = []

        # Apply template Matching
        count = 0
        while True:
            count += 1
            res = cv2.matchTemplate(image, template, method, template_mask)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val < threshold:
                self.debug('{0} < {1}'.format(max_val, threshold))
                break
            else:
                self.debug('{0} > {1}'.format(max_val, threshold))

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            top_left = max_loc
            bottom_right = (top_left[0] + width, top_left[1] + height)

            # Hide match under black rectangle:
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), -1)

            if region:
                top_left = (top_left[0] + x1, top_left[1] + y1)
                bottom_right = (bottom_right[0] + x1, bottom_right[1] + y1)
            item = MySkyMenuItem(top_left, bottom_right)
            menu_items.append(item)

        menu_items.sort(key=lambda x: x.top_left[1])
        return menu_items

    def find_image_menu_items(self):
        """Function to find the menu items with an image in the image.
        This function will return only menu elements with images on them ordered by vertical position.

        Returns:
            List of the menu items found
        """

        template = cv2.imread(IMAGE_BORDER, cv2.IMREAD_COLOR)
        mask = cv2.imread(IMAGE_MASK, cv2.IMREAD_COLOR)
        menu_items = self.generic_item_find(template, TM_CCOEFF_THRESHOLD_BOX_ITEM, mask, region=MY_SKY_REGION)

        for item in menu_items:
            item.text, item.selected = self.get_image_menu_item_text(item.region)

        if self.debug_mode and self.show_images_results:
            self.plot_results(menu_items, region=MY_SKY_REGION)

        return menu_items

    def find_text_menu_items(self):
        """Function to find the menu items with only text in the image.
        This function will return only menu elements with text on them ordered by vertical position.

        Returns:
            List of the menu items found
        """

        # This will find the only selected menu item:
        template = cv2.imread(IMAGE_BORDER_SMALL, cv2.IMREAD_COLOR)
        mask = cv2.imread(IMAGE_MASK_SMALL, cv2.IMREAD_COLOR)
        menu_items = self.generic_item_find(template, TM_CCOEFF_THRESHOLD_TEXT_ITEM, mask, region=MY_SKY_REGION)
        if not menu_items:
            return []

        # Mark the found item as selected:
        menu_items[0].selected = True

        # Try to find not selected items, based on size and OCR results (later)
        selected_item = menu_items[0]
        region_top = MY_SKY_TEXT_MENU_REGION[0][1]
        region_bottom = MY_SKY_TEXT_MENU_REGION[1][1]

        # Search up:
        point = selected_item.top_left[1]
        while point >= region_top:
            self.debug('Top: {0}, Point: {1}'.format(region_top, point))
            point -= VERTICAL_TEXT_SIZE
            if point >= region_top:
                top_left = (selected_item.top_left[0], point)
                bottom_right = (selected_item.bottom_right[0], point + VERTICAL_TEXT_SIZE)
                item = MySkyMenuItem(top_left, bottom_right)
                item.selected = False
                menu_items.append(item)
            else:
                break

        # Search down:
        point = menu_items[0].bottom_right[1]
        while point <= region_bottom:
            self.debug('Bottom: {0}, Point: {1}'.format(region_bottom, point))
            if point + VERTICAL_TEXT_SIZE <= region_bottom:
                top_left = (selected_item.top_left[0], point)
                bottom_right = (selected_item.bottom_right[0], point + VERTICAL_TEXT_SIZE)
                item = MySkyMenuItem(top_left, bottom_right)
                item.selected = False
                menu_items.append(item)
            else:
                break
            point += VERTICAL_TEXT_SIZE

        for item in menu_items:
            item.text = self.find_text(item.region)

        # Clean and sort results:
        menu_items = [item for item in menu_items if item.text]
        menu_items.sort(key=lambda x: x.top_left[1])

        if self.debug_mode and self.show_images_results:
            self.plot_results(menu_items, region=MY_SKY_TEXT_MENU_REGION)

            for item in menu_items:
                self.show_pillow_image(item.region)

        return menu_items


    def plot_results(self, menu_items, region=None):
        """Function to plot the menus found in an image.

        Args:
            menu_items (list(MySkyMenuItem)): List of menu items found
            region (tuple(tuple(int))): Region of the image analysed defined by the top-left and bottom-right coordinates
        """
        print_image = self.image.copy()

        if region:
            cv2.rectangle(print_image, region[0], region[1], 255, 2)

        count = 0
        for item in menu_items:
            self.debug('Item {0}: ({1}, {2})'.format(count, item.top_left, item.bottom_right))
            if item.selected:
                color = (0, 0, 255)
            else:
                color = (255, 255, 255)
            cv2.rectangle(print_image, item.top_left, item.bottom_right, color, 2)
            count += 1

        show_numpy_image(print_image, 'Detected Point', 'Method: TM_CCOEFF', convert=cv2.COLOR_BGR2RGB)

    def get_image_menu_item_text(self, region):
        """Read the text in the given region and tell if the menu item is selected or not

        Args:
            region (tuple(tuple(int))): Region of the image to search defined by the top-left and bottom-right coordinates

        Returns:
            Text and selection status of the given item
        """
        text = 'DUMMY'
        selected = False

        x1 = region[0][0] + HORIZONAL_TEXT_MARGIN
        x2 = region[1][0] - HORIZONAL_TEXT_MARGIN
        y1 = region[1][1] - VERTICAL_TEXT_SIZE_WITH_IMAGE
        y2 = region[1][1]

        text_region = ((x1, y1), (x2, y2))
        text = self.find_text(text_region).strip()

        if self.debug_mode and self.show_images_results:
            self.show_pillow_image(text_region)

        # Find out if selected or not
        # Exclude text color from the search:
        color = dominant_color(self.image, region, exclude_list=[BLACK_RGB, WHITE_RGB])
        selected = is_similar_color_rgb(bgr_to_rgb(color), YELLOW_BACKGROUND_RGB)

        return text, selected

    def find_text(self, region):
        """Read the text in the given region

        Args:
            region (tuple(tuple(int))): Region of the image to search defined by the top-left and bottom-right coordinates

        Returns:
            Text of the given item
        """
        cropped_image = crop_image(self.image, region)
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        pil_image = Image.fromarray(np.rollaxis(cropped_image, 0, 1))
        if self.debug_mode and self.show_images_results:
            pil_image.show()

        with tesserocr.PyTessBaseAPI() as api:
            api.SetImage(pil_image)
            api.SetVariable('tessedit_char_whitelist', OCR_CHAR_WHITELIST)
            text = api.GetUTF8Text().strip().encode('utf-8')
            if text:
                text = self.fuzzy_match(text)
            self.debug('Found text: {0}'.format(text))
            return text

    def show_pillow_image(self, region):
        """Show the given image region on the screen

        Args:
            region (tuple(tuple(int))): Region of the image to show defined by the top-left and bottom-right coordinates
        """
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cropped_image = crop_image(rgb_image, region)
        pil_image = Image.fromarray(np.rollaxis(cropped_image, 0, 1))
        pil_image.show()

    def fuzzy_match(self, text):
        """Get the text fuzzy matched against our dictionary

        Args:
            text (str): Text to match

        Returns:
            Matched text
        """
        matches = self.fuzzy_set.get(text)
        # We get directly the most likely match
        return matches[0][1]

    def contour_detection(self, region=None):
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cropped_image = crop_image(image_gray, region)
        blurred_image = cv2.medianBlur(cropped_image, 5)
        threshold_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        _, contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        # Move contours to absolute coordinates
        if region:
            region_x = region[0][0]
            region_y = region[0][1]
            for cont in contours:
                for point in cont:
                    point[0][0] += region_x
                    point[0][1] += region_y

        filtered_contours = []
        for cont in contours:
            # approximate the contour
            peri = cv2.arcLength(cont, True)
            approximation = 0.01
            approx = cv2.approxPolyDP(cont, approximation * peri, True)
         
            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                filtered_contours.append(approx)
                continue
        self.debug('Found {0} contours'.format(len(filtered_contours)))

        # Get bounding boxes for contours:
        bounding_box = lambda cont: cv2.boundingRect(cont)
        boxes = [cv2.boundingRect(cont) for cont in filtered_contours]
        self.debug('boxes: {0}'.format(boxes))

        # Remove boxes close to region:
        if region:
            region_box = (region[0][0], region[0][1], region[1][0] - region[0][0], region[1][1] - region[0][1])
            close_to_region = lambda b: boxes_are_similar(b, region_box)
            boxes = [box for box in boxes if not close_to_region(box)]

        # Get box groups:
        groups = []
        for box in boxes:
            if not groups:
                group = [box]
                groups.append(group)
            matched = False
            for group in groups:
                if boxes_are_similar(group[0], box):
                    matched = True
                    group.append(box)
                    break
            if matched:
                continue
            else:
                group = [box]
                groups.append(group)
        self.debug('Groups: {0}'.format(groups))

        # Get group intersections:
        inner_boxes = []
        for group in groups:
            new_box = group[0]
            for box in group:
                intersect = intersection(new_box, box)
                if intersect is not None:
                    new_box = intersect
            inner_boxes.append(new_box)
        self.debug('inner_boxes: {0}'.format(inner_boxes))

        # Clean redundant inner boxes:
        outer_boxes = []
        for box in inner_boxes:
            inside = False
            for box2 in inner_boxes:
                if box == box2:
                    continue
                if is_inside(box2, box):
                    inside = True
            if not inside:
                outer_boxes.append(box)
        outer_boxes = list(set(outer_boxes))
        self.debug('outer_boxes: {0}'.format(outer_boxes))



        if self.debug_mode and self.show_images_results:
            image2 = self.image.copy()
            cv2.drawContours(image2, contours, -1, (0,255,0), 1)
            show_numpy_image(image2, 'Contour detection', 'All contours', convert=cv2.COLOR_BGR2RGB)

            image3 = self.image.copy()
            cv2.drawContours(image3, filtered_contours, -1, (0,255,0), 1)
            show_numpy_image(image3, 'Contour detection', 'Filtered contours', convert=cv2.COLOR_BGR2RGB)

            image4 = self.image.copy()
            for box in boxes:
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
                cv2.rectangle(image4, (x, y), (x+w, y+h), (0, 255, 0), 1)
            show_numpy_image(image4, 'Contour detection', 'Square contours', convert=cv2.COLOR_BGR2RGB)

            image5 = self.image.copy()
            for box in inner_boxes:
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
                cv2.rectangle(image5, (x, y), (x+w, y+h), (0, 255, 0), 1)
            show_numpy_image(image5, 'Contour detection', 'Grouped boxes', convert=cv2.COLOR_BGR2RGB)

            image6 = self.image.copy()
            for box in outer_boxes:
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
                cv2.rectangle(image6, (x, y), (x+w, y+h), (0, 255, 0), 1)
            show_numpy_image(image6, 'Contour detection', 'Inner boxes cleaned', convert=cv2.COLOR_BGR2RGB)

        return outer_boxes

####################
### TESTING CODE ###
####################

def test_function():
    testing_image = cv2.imread(TEST_IMAGE_MYSKY_HOME, cv2.IMREAD_COLOR)
    #testing_image = cv2.imread(TEST_IMAGE_MYSKY_MENU, cv2.IMREAD_COLOR)
    #testing_image = cv2.imread(TEST_IMAGE_MYSKY_MENU_1, cv2.IMREAD_COLOR)
    instance = SkyPlusTestUtils(testing_image, debug_mode=True, show_images_results=True)

    instance.contour_detection(MY_SKY_REGION)
    return 0
    menu_item_list = instance.find_image_menu_items()

    for menu_item in menu_item_list:
        print 'Item: [{0}] {1}, ({2})'.format(menu_item.selected, menu_item.text.encode('utf-8'), menu_item.region)

    testing_image = cv2.imread(TEST_IMAGE_MYSKY_MENU, cv2.IMREAD_COLOR)
    instance = SkyPlusTestUtils(testing_image, debug_mode=True, show_images_results=True)
    menu_item_list = instance.find_image_menu_items()

    for menu_item in menu_item_list:
        print 'Item: [{0}] {1}, ({2})'.format(menu_item.selected, menu_item.text.encode('utf-8'), menu_item.region)

    testing_image = cv2.imread(TEST_IMAGE_MYSKY_MENU_1, cv2.IMREAD_COLOR)
    instance = SkyPlusTestUtils(testing_image, debug_mode=True, show_images_results=True)
    menu_item_list = instance.find_text_menu_items()

    for menu_item in menu_item_list:
        print 'Item: [{0}] {1}, ({2})'.format(menu_item.selected, menu_item.text.encode('utf-8'), menu_item.region)

    print 'Finish'

if __name__ == '__main__':
    test_function()

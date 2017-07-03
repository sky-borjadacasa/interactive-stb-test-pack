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

import os
import importlib
import string
install_and_import('cv2', 'opencv-python')
install_and_import('numpy')
import numpy as np

os.system('sudo apt-get -y install python-scipy')
install_and_import('scipy.stats', 'scipy')
from scipy.stats import itemfreq

os.system('sudo pip install fuzzyset')
install_and_import('fuzzyset')
from fuzzyset import FuzzySet

# Try to import testing libs:
try:
    install_and_import('PIL', 'pillow')
    install_and_import('matplotlib')
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
    install_and_import('tesserocr')

# Constants:
TM_CCOEFF_THRESHOLD_BOX_ITEM = 250000000
TM_CCOEFF_THRESHOLD_TEXT_ITEM = 140000000
VERTICAL_TEXT_SIZE = 50
VERTICAL_TEXT_SIZE_WITH_IMAGE = 50
HORIZONAL_TEXT_MARGIN = 10
BOX_SIMILARITY_THRESHOLD = 10

# Regions:
MY_SKY_REGION = ((880, 0), (1280 - 1, 720 - 1)) # The 400 pixels to the right and the whole height of the screen
MY_SKY_GREETING_REGION = ((930, 90), (1230, 135))
MY_SKY_TEXT_MENU_REGION = ((920, 125), (1240, 550))

# Text recognition:
OCR_CHAR_WHITELIST = string.ascii_letters + ' ' + string.digits

# Colors:
YELLOW_BACKGROUND_RGB = np.array([235, 189, 0])
BLUE_BACKGROUND_RGB = np.array([30, 87, 161])
BLACK_RGB = np.array([0, 0, 0])
WHITE_RGB = np.array([255, 255, 255])
COLOR_THRESHOLD = 10
PALETTE_SIZE = 3

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
        'Good Afternoon']
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


def intersection(a, b):
    """Calculate the intersection of two regions

    Args:
        a (tuple): Tuple giving the x, y, width and height of region
        b (tuple): Tuple giving the x, y, width and height of region

    Returns:
        Intersection of both regions or None if there's no intersection
    """
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0] + a[2], b[0] + b[2]) - x
    h = min(a[1] + a[3], b[1] + b[3]) - y
    if w < 0 or h < 0:
        return None
    return (x, y, w, h)

def is_inside(a, b):
    """Say if region b is inside region a

    Args:
        a (tuple): Tuple giving the x, y, width and height of region
        b (tuple): Tuple giving the x, y, width and height of region

    Returns:
        True if b is inside a, False otherwise
    """
    x_distance = a[0] - b[0]
    y_distance = a[1] - b[1]
    w_distance = a[0] + a[2] - b[0] - b[2]
    h_distance = a[1] + a[3] - b[1] - b[3]
    return x_distance <= 0 and y_distance <= 0 \
        and w_distance >= 0 and h_distance >= 0

def boxes_are_similar(a, b):
    """Say if two boxes are similar (i.e., line distances are under a maximum threshold)

    Args:
        a (tuple): Tuple giving the x, y, width and height of region
        b (tuple): Tuple giving the x, y, width and height of region

    Returns:
        True if boxes are similar
    """
    size_threshold = BOX_SIMILARITY_THRESHOLD
    x_distance = abs(a[0] - b[0])
    y_distance = abs(a[1] - b[1])
    w_distance = abs(a[0] + a[2] - b[0] - b[2])
    h_distance = abs(a[1] + a[3] - b[1] - b[3])
    return x_distance < size_threshold and y_distance < size_threshold \
        and w_distance < size_threshold and h_distance < size_threshold

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

def is_cv_version2():
    (major, minor, _) = cv2.__version__.split(".")
    return major == '2'

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

    def find_text_menu_items(self):
        """Function to find the menu items with only text in the image.
        This function will return only menu elements with text on them ordered by vertical position.

        Returns:
            List of the menu items found
        """

        # This will find the only selected menu item:
        menu_items = self.get_menu_items(MY_SKY_TEXT_MENU_REGION)

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
            item.text, _ = self.find_text_in_box(item.region)

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
        text, selected = self.find_text_in_box(text_region)
        text = text.strip()

        if self.debug_mode and self.show_images_results:
            self.show_pillow_image(text_region)

        return text, selected

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
            text = stbt.ocr(region=get_stbt_region(region)).strip().encode('utf-8')
            if text:
                text = self.fuzzy_match(text)
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
        selected = is_color_in_palette(palette, color_frequency, YELLOW_BACKGROUND_RGB)

        self.debug('Found text: {0}, {1}'.format(text, selected))

        return text, selected

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
        self.debug('Matches for "{0}":\n{1}'.format(text, matches))
        # We get directly the most likely match
        return matches[0][1]

    def contour_detection(self, region=None, include_region=False):
        """Get contours found in the image or given region to find menu items later

        Args:
            region (tuple(tuple(int))): Region to crop
            include_region (bool): Weather to include the region in the found boxes or not

        Returns:
            List of boxes found orderer by vertical position
        """
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cropped_image = crop_image(image_gray, region)
        blurred_image = cv2.medianBlur(cropped_image, 5)
        threshold_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        conts_return = cv2.findContours(threshold_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if is_cv_version2():
            contours = conts_return[0]
        else:
            contours = conts_return[1]
        # TODO: Fine tune this value or extract to constant
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
            # Approximate the contour:
            perimeter = cv2.arcLength(cont, True)
            approximation = 0.01
            approx = cv2.approxPolyDP(cont, approximation * perimeter, True)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                filtered_contours.append(approx)
                continue
        self.debug('Found {0} contours'.format(len(filtered_contours)))

        # Get bounding boxes for contours:
        boxes = [cv2.boundingRect(cont) for cont in filtered_contours]
        self.debug('boxes: {0}'.format(boxes))

        # Remove boxes close to region:
        if region and not include_region:
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

        # Print steps for debugging
        if self.debug_mode and self.show_images_results:
            image2 = self.image.copy()
            cv2.drawContours(image2, contours, -1, (0, 255, 0), 1)
            show_numpy_image(image2, 'Contour detection', 'All contours', convert=cv2.COLOR_BGR2RGB)

            image3 = self.image.copy()
            cv2.drawContours(image3, filtered_contours, -1, (0, 255, 0), 1)
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

        outer_boxes.sort(key=lambda box: box[1])
        return outer_boxes

    def get_menu_items(self, region=None):
        """Get menu items in the image or given region

        Args:
            region (tuple(tuple(int))): Region to find menu items

        Returns:
            List of menu items found orderer by vertical position
        """
        # XXX
        print 'REGION: {0}'.format(region)
        print 'REGION_C: {0}'.format(MY_SKY_REGION)

        boxes = self.contour_detection(region=region)

        menu_items = []
        for box in boxes:
            top_left = (box[0], box[1] + box[3] - VERTICAL_TEXT_SIZE_WITH_IMAGE)
            bottom_right = (box[0] + box[2], box[1] + box[3])
            text_region = (top_left, bottom_right)

            top_left = (box[0], box[1])
            item = MySkyMenuItem(top_left, bottom_right)
            item.text, item.selected = self.find_text_in_box(text_region)
            menu_items.append(item)

        return menu_items

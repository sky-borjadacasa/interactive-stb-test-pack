#!/usr/bin/env python

import sky_plus_utils
import cv2

# Test image files:
TEST_IMAGE_MYSKY_HOME = 'screenshots/MySkyHome.png'
TEST_IMAGE_MYSKY_MENU = 'screenshots/MySkyMenu.png'
TEST_IMAGE_MYSKY_MENU_1 = 'screenshots/MySkyMenu1.png'

def test_function():
    """Test the functionality of this library with some screenshots
    """
    testing_image = cv2.imread(TEST_IMAGE_MYSKY_HOME, cv2.IMREAD_COLOR)
    instance = sky_plus_utils.SkyPlusTestUtils(testing_image, debug_mode=True, show_images_results=True)
    region = ((940, 240), (1220, 280))
    text, selected = instance.find_text_in_box(region)

    return 0


    testing_image = cv2.imread(TEST_IMAGE_MYSKY_HOME, cv2.IMREAD_COLOR)
    instance = sky_plus_utils.SkyPlusTestUtils(testing_image, debug_mode=True, show_images_results=True)
    menu_item_list = instance.get_menu_items(sky_plus_utils.MY_SKY_REGION)
    for menu_item in menu_item_list:
        print 'Item: [{0}] {1}, ({2})'.format(menu_item.selected, menu_item.text.encode('utf-8'), menu_item.region)

    testing_image = cv2.imread(TEST_IMAGE_MYSKY_MENU, cv2.IMREAD_COLOR)
    instance = sky_plus_utils.SkyPlusTestUtils(testing_image, debug_mode=True, show_images_results=True)
    menu_item_list = instance.get_menu_items(sky_plus_utils.MY_SKY_REGION)

    for menu_item in menu_item_list:
        print 'Item: [{0}] {1}, ({2})'.format(menu_item.selected, menu_item.text.encode('utf-8'), menu_item.region)

    testing_image = cv2.imread(TEST_IMAGE_MYSKY_MENU_1, cv2.IMREAD_COLOR)
    instance = sky_plus_utils.SkyPlusTestUtils(testing_image, debug_mode=True, show_images_results=True)
    menu_item_list = instance.find_text_menu_items()

    for menu_item in menu_item_list:
        print 'Item: [{0}] {1}, ({2})'.format(menu_item.selected, menu_item.text.encode('utf-8'), menu_item.region)

    print 'Finish'

if __name__ == '__main__':
    test_function()
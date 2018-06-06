#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Messages
"""

from time import sleep
import stbt
from sky_plus_utils import debug
from interactive_frame_objects import InteractiveMainMenu


# ##################### #
# ##### Constants ##### #
# ##################### #


MAX_MENU_LENGTH = 20


# ####################### #
# ##### Basic utils ##### #
# ####################### #


def clear_test():
    """Close any app"""
    sleep(2)
    stbt.press('KEY_SKY')
    sleep(3)


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
    assert len(channel) == 3, '[Go to channel] Channel should have 3 digits, but has {0}'.format(len(channel))
    press_digits(channel)


def open_secret_scene():
    """Open secret scene menu
    """
    press_digits('062840')


def select_menu(frame_object, menu_name, timeout_secs=10):
    """Select menu with the given name

    Args:
        frame_object (Class): Class of the Frame Object that can read this menu
        menu_name (str): Name of the menu to select
        timeout_secs (int): Timeout in seconds for finding the frame object
    """
    # Get the menus:
    # pylint: disable=stbt-wait-until-callable
    menu = stbt.wait_until(frame_object, timeout_secs=timeout_secs)

    # Check if the menu we want exists:
    menu_item = [x for x in menu.menu_items if x.text == menu_name]
    assert menu_item is not None, 'Menu item {0} not found in this screen'.format(menu_name)

    if menu.message == menu_name:
        return

    for i in range(0, MAX_MENU_LENGTH):
        # pylint: disable=stbt-wait-until-callable
        menu = stbt.wait_until(frame_object, timeout_secs=timeout_secs)
        debug('[SELECT_MENU] Screen {0} selected: {1}->{2}'.format(type(menu).__name__, i, menu.message))

        if menu.message == menu_name:
            debug('[SELECT_MENU] Item found: {0} -> {1}->{2}'.format(type(menu).__name__, i, menu.message))
            break
        stbt.press('KEY_DOWN')
        # Give STB 3 seconds to move the highlighted menu entry
        sleep(3)

    assert menu.message == menu_name, \
        '[SELECT_MENU] ({0}) Selected item is not [{1}]'.format(type(menu).__name__, menu_name)


def enter_menu(frame_object, menu_name, timeout_secs=10):
    """Select and enter menu with the given name

    Args:
        frame_object (Class): Class of the Frame Object that can read this menu
        menu_name (str): Name of the menu to enter
        timeout_secs (int): Timeout in seconds for finding the frame object
    """
    select_menu(frame_object, menu_name, timeout_secs)

    # Open menu:
    stbt.press('KEY_SELECT')


# ###################### #
# ##### Test utils ##### #
# ###################### #


def open_and_basic_check_interactive_menu():
    """Open the My Messages app and make basic checks"""
    stbt.press('KEY_INTERACTIVE')
    sleep(1)
    menu = stbt.wait_until(InteractiveMainMenu)
    assert menu.is_visible, '[Interactive] Main menu is not visible'

    menu_items = menu.menu_items
    for item in menu_items:
        debug('Item text: {0}'.format(item.text))
        debug('Item selected: {0}'.format(item.selected))
    assert len(menu_items) == 9, '[Interactive] Main menu should have 9 items, but has {0}'.format(len(menu_items))
    return menu

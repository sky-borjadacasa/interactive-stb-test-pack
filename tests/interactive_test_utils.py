#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Messages
"""

from time import sleep
import stbt
from sky_plus_utils import debug
from interactive_frame_objects import InteractiveMainMenu, MAIN_MENU_ITEM_REGIONS


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


# TODO: Create select menu
def enter_menu(menu_name):
    """Select menu with the given name

    Args:
        menu_name (str): Name of the menu to open
    """
    # Navigate menus:
    menu = None
    # pylint: disable=unused-variable
    # TODO: Review this logic
    for i in range(0, len(MAIN_MENU_ITEM_REGIONS)):
        menu = stbt.wait_until(InteractiveMainMenu, timeout_secs=20)
        debug('[INTERACTIVE_MENU] Item selected: {0}'.format(menu.message))

        if menu.message == menu_name:
            debug('[INTERACTIVE_MENU] Item found!: {0}'.format(menu.message))
            break
        debug('[INTERACTIVE_MENU] Press DOWN')
        stbt.press('KEY_DOWN')
        # Give STB 3 seconds to move the highlighted menu entry
        sleep(3)

    assert menu.message == menu_name, \
        '[INTERACTIVE_MENU] Selected item is not [{0}]'.format(menu_name)

    # Open My Messages:
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
    debug(len(menu_items))
    assert len(menu_items) == 9, '[Interactive] Main menu should have 9 items, but has {0}'.format(len(menu_items))
    return menu

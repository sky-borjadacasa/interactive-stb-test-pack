#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Messages
"""

from time import sleep
import stbt
from sky_plus_utils import debug
from interactive_constants import MAIN_MENU_ITEM_REGIONS
from interactive_frame_objects import InteractiveMainMenu

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

def enter_menu(menu_name):
    """Select menu with the given name

    Args:
        menu_name (str): Name of the menu to open
    """
    # Navigate menus:
    menu = None
    # pylint: disable=unused-variable
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

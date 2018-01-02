#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Messages
"""

from time import sleep
import stbt
from sky_plus_utils import debug
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

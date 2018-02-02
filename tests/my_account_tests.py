#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Account
"""

from time import sleep
import stbt
import sky_plus_utils
from sky_plus_utils import clear_test, debug
from interactive_frame_objects import InteractiveMainMenu, MyAccountMenu
import interactive_constants
from interactive_constants import MAIN_MENU_ITEM_REGIONS
import sky_plus_strings
from interactive_test_utils import open_and_basic_check_interactive_menu

def test_smoke_open_my_account():
    """Open MySky app"""
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        # XXX Get menu here?
        menu = open_and_basic_check_interactive_menu()

        # Navigate menus:
        # pylint: disable=unused-variable
        for i in range(0, len(MAIN_MENU_ITEM_REGIONS)):
            menu = stbt.wait_until(InteractiveMainMenu, timeout_secs=20)
            debug('[INTERACTIVE_MENU] Item selected: {0}'.format(menu.message))

            # Wait 3 secs and check
            sleep(3)
            if menu.message == sky_plus_strings.MY_ACCOUNT:
                debug('[INTERACTIVE_MENU] Item found!: {0}'.format(menu.message))
                break
            debug('[INTERACTIVE_MENU] Press DOWN')
            stbt.press('KEY_DOWN')
        # XXX Is this needed?
        # assert stbt.wait_until(lambda: InteractiveMainMenu().message == sky_plus_strings.MY_ACCOUNT, timeout_secs=20), \
        #     '[Interactive] Selected item is not [{0}]'.format(sky_plus_strings.MY_ACCOUNT)
        assert menu.message == sky_plus_strings.MY_ACCOUNT, \
            '[Interactive] Selected item is not [{0}]'.format(sky_plus_strings.MY_ACCOUNT)

        # Open My Messages:
        stbt.press('KEY_SELECT')
        ma_menu = stbt.wait_until(MyAccountMenu, timeout_secs=20)
        assert ma_menu.is_visible, '[My Account] Menu is not visible'
    finally:
        clear_test()

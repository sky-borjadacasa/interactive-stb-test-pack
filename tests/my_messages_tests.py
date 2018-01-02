#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Messages
"""

import stbt
import sky_plus_utils
from sky_plus_utils import clear_test
from interactive_frame_objects import InteractiveMainMenu, MyMessagesMenu
import interactive_constants
import sky_plus_strings
from interactive_test_utils import open_and_basic_check_interactive_menu

def test_smoke_open_my_messages():
    """Open MySky app"""
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        open_and_basic_check_interactive_menu()

        # Navigate menus:
        stbt.press('KEY_DOWN')
        stbt.press('KEY_DOWN')
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: InteractiveMainMenu().message == sky_plus_strings.MY_MESSAGES, timeout_secs=20), \
            '[Interactive] Selected item is not [{0}]'.format(sky_plus_strings.MY_MESSAGES)

        # Open My Messages:
        stbt.press('KEY_SELECT')
        menu = stbt.wait_until(MyMessagesMenu)
        assert menu.is_visible, '[My Messages] Menu is not visible'
    finally:
        clear_test()

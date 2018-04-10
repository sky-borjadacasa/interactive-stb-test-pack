#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Account
"""

import stbt
import sky_plus_utils
from sky_plus_utils import clear_test
from interactive_frame_objects import MyAccountMenu
import interactive_constants
import sky_plus_strings
from interactive_test_utils import open_and_basic_check_interactive_menu, enter_menu

def test_smoke_open_my_account():
    """Open MySky app"""
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE_HD)
        open_and_basic_check_interactive_menu()
        enter_menu(sky_plus_strings.MY_ACCOUNT)

        menu = stbt.wait_until(MyAccountMenu, timeout_secs=20)
        assert menu.is_visible, '[My Account] Menu is not visible'
    finally:
        clear_test()

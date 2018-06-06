#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Account
"""

import stbt
from interactive_frame_objects import MyAccountMenu
import interactive_constants
import sky_plus_strings
import interactive_test_utils as itu


def test_smoke_open_my_account():
    """Open MySky app"""
    itu.clear_test()
    try:
        itu.go_to_channel(interactive_constants.CHANNEL_SKY_ONE_HD)
        itu.open_and_basic_check_interactive_menu()
        itu.enter_menu(sky_plus_strings.MY_ACCOUNT)

        menu = stbt.wait_until(MyAccountMenu, timeout_secs=20)
        assert menu.is_visible, '[My Account] Menu is not visible'
    finally:
        itu.clear_test()

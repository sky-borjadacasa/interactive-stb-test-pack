#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for My Messages
"""

import stbt
from interactive_frame_objects import MyMessagesMenu, InteractiveMainMenu
import interactive_constants
import sky_plus_strings
import interactive_test_utils as itu


def test_smoke_open_my_messages():
    """Open MySky app"""
    itu.clear_test()
    try:
        itu.go_to_channel(interactive_constants.CHANNEL_SKY_ONE_HD)
        itu.open_and_basic_check_interactive_menu()
        itu.enter_menu(InteractiveMainMenu, sky_plus_strings.MY_ACCOUNT, timeout_secs=20)

        menu = stbt.wait_until(MyMessagesMenu)
        assert menu.is_visible, '[My Messages] Menu is not visible'
    finally:
        itu.clear_test()

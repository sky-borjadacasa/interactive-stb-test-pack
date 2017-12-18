#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test cases for MySky
"""

import stbt
import sky_plus_utils
from mysky_frame_objects import SecretSceneMainMenu, DeveloperMenuMenu
import mysky_constants
import mysky_test_utils

def test_setup_backend():
    """Set up backend environment"""
    mysky_test_utils.clear_test()
    try:
        sky_plus_utils.go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        mysky_test_utils.open_and_basic_check_mysky()
        sky_plus_utils.open_secret_scene()

        # pylint: disable=stbt-unused-return-value
        stbt.wait_until(SecretSceneMainMenu)
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: SecretSceneMainMenu().message == mysky_constants.STRING_SS_DEVELOPER_MODE), \
            '[Secret Scene] Selected item is not [{0}]'.format(mysky_constants.STRING_SS_DEVELOPER_MODE)
        stbt.press('KEY_SELECT')
        dev_mode_menu = stbt.wait_until(DeveloperMenuMenu)
        assert dev_mode_menu.title == mysky_constants.STRING_SS_VCN, \
            '[Developer Mode] Selected item is not [{0}]'.format(mysky_constants.STRING_SS_VCN)
    finally:
        mysky_test_utils.clear_test()

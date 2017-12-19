#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test cases for MySky
"""

from time import sleep
import stbt
import sky_plus_utils
from mysky_frame_objects import SecretSceneMainMenu, DeveloperMenuMenu, detect_moving_balls
import mysky_constants
import mysky_test_utils

# Secret scene environment codes:
ENV_CODE_DEV = 'KEY_0'
ENV_CODE_SIT = 'KEY_1'
ENV_CODE_STAGE = 'KEY_2'
ENV_CODE_PROD = 'KEY_3'

def open_developer_mode(env_code):
    """Open Developer mode"""
    mysky_test_utils.clear_test()
    try:
        sky_plus_utils.go_to_channel(mysky_constants.CHANNEL_SKY_ONE)
        mysky_test_utils.open_and_basic_check_mysky()
        # XXX
        assert stbt.wait_until(lambda: not detect_moving_balls(stbt.Frame)), \
            '[MOVING BALLS] Moving balls didn\'t disappear'
        # XXX
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
        stbt.press(env_code)
        sleep(2)
    finally:
        mysky_test_utils.clear_test()

def test_setup_backend_dev():
    """Set up backend environment"""
    open_developer_mode(ENV_CODE_DEV)

def test_setup_backend_sit():
    """Set up backend environment"""
    open_developer_mode(ENV_CODE_SIT)

def test_setup_backend_stage():
    """Set up backend environment"""
    open_developer_mode(ENV_CODE_STAGE)

def test_setup_backend_prod():
    """Set up backend environment"""
    open_developer_mode(ENV_CODE_PROD)

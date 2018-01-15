#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test cases for MySky
"""

from time import sleep
import stbt
import sky_plus_utils
from sky_plus_utils import clear_test
import mysky_frame_objects
from mysky_frame_objects import SecretSceneMainMenu, DeveloperMenuMenu
import interactive_constants
import sky_plus_strings

# Secret scene environment codes:
ENV_CODE_DEV = 'KEY_0'
ENV_CODE_SIT = 'KEY_1'
ENV_CODE_STAGE = 'KEY_2'
ENV_CODE_PROD = 'KEY_3'

def open_developer_mode(env_code):
    """Open Developer mode"""
    clear_test()
    try:
        sky_plus_utils.go_to_channel(interactive_constants.CHANNEL_SKY_ONE)
        mysky_frame_objects.open_and_basic_check_mysky()
        sleep(0.5)
        sky_plus_utils.open_secret_scene()

        # pylint: disable=stbt-unused-return-value
        stbt.wait_until(SecretSceneMainMenu)
        stbt.press('KEY_DOWN')
        assert stbt.wait_until(lambda: SecretSceneMainMenu().message == sky_plus_strings.SS_DEVELOPER_MODE), \
            '[Secret Scene] Selected item is not [{0}]'.format(sky_plus_strings.SS_DEVELOPER_MODE)
        stbt.press('KEY_SELECT')
        dev_mode_menu = stbt.wait_until(DeveloperMenuMenu)
        assert dev_mode_menu.title == sky_plus_strings.SS_VCN, \
            '[Developer Mode] Selected item is not [{0}]'.format(sky_plus_strings.SS_VCN)
        stbt.press(env_code)
        sleep(2)
    finally:
        clear_test()

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

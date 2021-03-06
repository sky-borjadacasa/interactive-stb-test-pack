#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test cases for MySky
"""

from time import sleep
import stbt
from sky_plus_utils import debug
import interactive_test_utils as itu
import mysky_frame_objects
from mysky_frame_objects import SecretSceneMainMenu, DeveloperModeMenu
import interactive_constants
import sky_plus_strings
import test_scenario_manager

# Secret scene environment codes:
ENV_CODE_DEV = 'KEY_0'
ENV_CODE_SIT = 'KEY_1'
ENV_CODE_STAGE = 'KEY_2'
ENV_CODE_PROD = 'KEY_3'


def open_developer_mode():
    """Open Developer mode"""
    itu.go_to_channel(interactive_constants.CHANNEL_SKY_ONE_HD)
    mysky_frame_objects.open_and_basic_check_mysky()
    sleep(0.5)
    itu.open_secret_scene()

    itu.enter_menu(SecretSceneMainMenu, sky_plus_strings.SS_DEVELOPER_MODE)

    dev_mode_menu = stbt.wait_until(DeveloperModeMenu)
    assert dev_mode_menu.title == sky_plus_strings.SS_VCN, \
        '[Developer Mode] Selected item is not [{0}]'.format(sky_plus_strings.SS_VCN)


def setup_backend(env_code):
    """Open Developer mode"""
    itu.clear_test()
    try:
        open_developer_mode()
        stbt.press(env_code)
        sleep(2)
    finally:
        itu.clear_test()


def test_setup_backend_dev():
    """Set up backend environment"""
    setup_backend(ENV_CODE_DEV)


def test_setup_backend_sit():
    """Set up backend environment"""
    setup_backend(ENV_CODE_SIT)


def test_setup_backend_stage():
    """Set up backend environment"""
    setup_backend(ENV_CODE_STAGE)


def test_setup_backend_prod():
    """Set up backend environment"""
    setup_backend(ENV_CODE_PROD)


# ################ #
# ### HD utils ### #
# ################ #

def test_setup_disable_hd():
    """Disable HD"""
    itu.clear_test()
    try:
        open_developer_mode()
        itu.enter_menu(DeveloperModeMenu, sky_plus_strings.SSD_DISABLE_HD, timeout_secs=20)
        sleep(2)
    finally:
        itu.clear_test()


def test_setup_enable_hd():
    """Enable HD"""
    itu.clear_test()
    try:
        open_developer_mode()
        itu.enter_menu(DeveloperModeMenu, sky_plus_strings.SSD_ENABLE_HD, timeout_secs=20)
        sleep(2)
    finally:
        itu.clear_test()


# ################# #
# ### VCN utils ### #
# ################# #


def setup_vcn(vcn):
    """Set fake VCN"""
    itu.clear_test()
    try:
        debug('[SETTING VCN]: {0}'.format(vcn))
        open_developer_mode()
        stbt.press('KEY_UP')
        sleep(5)
        # pylint: disable=unused-variable
        for i in range(0, 9):
            stbt.press('KEY_LEFT')
            sleep(0.1)
        itu.press_digits(vcn)
        sleep(5)
        stbt.press('KEY_DOWN')
        # pylint: disable=stbt-unused-return-value
        stbt.wait_until(SecretSceneMainMenu)
    finally:
        itu.clear_test()


def test_setup_vcn_any():
    """Set any VCN"""
    vcn = test_scenario_manager.get_any_vcn()
    setup_vcn(vcn)


def test_setup_vcn_vip():
    """Set any VCN"""
    vcn = test_scenario_manager.get_vip_vcn()
    setup_vcn(vcn)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Strings for Sky Plus testing
"""

import string

# Text recognition:
OCR_CHAR_WHITELIST = string.ascii_letters + ' ' + string.digits
OCR_CHAR_WHITELIST_TEMP = string.digits + '-ºc'
OCR_CHAR_WHITELIST_PIN = string.digits + '_'

# MySky:
MANAGE_YOUR_ACCOUNT = 'Manage your account'
FIX_A_PROBLEM = 'Fix a problem'
YOUR_FORECAST = 'Your forecast'
BILLS_AND_PAYMENTS = 'Bills and Payments'
PACKAGE_AND_SETTINGS = 'TV package and settings'
BROADBAND_AND_TALK = 'Broadband and Talk'
DETAILS_AND_MESSAGES = 'My details and messages'
PICTURE_PROBLEMS = 'TV picture problems'
NO_SATELITE_SIGNAL = 'No satelite signal'
FORGOTTEN_PIN = 'Forgotten PIN'
EXPLORE_MORE = 'Explore more'
LOADING = 'Loading...'
NEXT_GENERATION = 'The next generation box'
YOUR_LOCAL_WEATHER = 'Your local weather'
INTERACTIVE_MY_SKY = 'Interactive My Sky'
SS_CLOSE_POPUP = 'Close this popup'
SS_DEVELOPER_MODE = 'Developer mode'
SS_VCN = 'VCN'
SSD_SCRATCH = 'Scratch test menu'
SSD_DUMP_STATE = 'Dump state to serial'
SSD_DUMP_AV_INFO = 'Dump AV info to serial'
SSD_CV_LIVE = 'Content version \'live\''
SSD_CV_PREVIEW = 'Content version \'preview\''
SSD_ENABLE_HD = 'Enable HD'
SSD_DISABLE_HD = 'Disable HD'
SSD_GENERATE_FONTS_MAP = 'Generate fonts map'

# Interactive Main Menu:
INTERACTIVE = 'Interactive'
HELP_AND_SUPPORT = 'Help and Support'
GET_HELP = 'Get help with Sky\'s products and services'
RESET_TV_PIN = 'Reset TV PIN'
UPDATE_EMAIL = 'Update Email Address'
MY_MESSAGES = 'My Messages'
LAUNCHPAD = 'launchpad'
STB_DEV_APP = 'STB Dev App'
MY_SKY = 'MySky'
MY_ACCOUNT = 'My Account'
SKY_SHOP = 'Sky Shop'

# My Messages Menu:
MM_SUBTITLE = 'My Messages may contain personal account information.'

# Fuzzy set:
FUZZY_SET = [MANAGE_YOUR_ACCOUNT,
             FIX_A_PROBLEM,
             YOUR_FORECAST,
             BILLS_AND_PAYMENTS,
             PACKAGE_AND_SETTINGS,
             BROADBAND_AND_TALK,
             DETAILS_AND_MESSAGES,
             PICTURE_PROBLEMS,
             NO_SATELITE_SIGNAL,
             FORGOTTEN_PIN,
             EXPLORE_MORE,
             LOADING,
             NEXT_GENERATION,
             YOUR_LOCAL_WEATHER,
             INTERACTIVE_MY_SKY,
             SS_CLOSE_POPUP,
             SS_DEVELOPER_MODE,
             SS_VCN,
             SSD_SCRATCH,
             SSD_DUMP_STATE,
             SSD_DUMP_AV_INFO,
             SSD_CV_LIVE,
             SSD_CV_PREVIEW,
             SSD_ENABLE_HD,
             SSD_DISABLE_HD,
             SSD_GENERATE_FONTS_MAP,
             INTERACTIVE,
             HELP_AND_SUPPORT,
             GET_HELP,
             RESET_TV_PIN,
             UPDATE_EMAIL,
             MY_MESSAGES,
             LAUNCHPAD,
             STB_DEV_APP,
             MY_SKY,
             MY_ACCOUNT,
             SKY_SHOP,
             MM_SUBTITLE]

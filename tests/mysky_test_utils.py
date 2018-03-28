#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import datetime
import stbt
from stbt import Region
from sky_plus_utils import debug
import mysky_constants
import sky_plus_strings

def greeting_string():
    """Get greeting string"""
    now = datetime.datetime.now()
    debug('Datetime now: {0}'.format(now))
    mid_day_string = "12:00:00"
    mid_day = datetime.datetime.strptime(mid_day_string, "%H:%M:%S")
    mid_day = now.replace(hour=mid_day.time().hour, minute=mid_day.time().minute, \
        second=mid_day.time().second, microsecond=0)
    six_pm_string = "18:00:00"
    six_pm = datetime.datetime.strptime(six_pm_string, "%H:%M:%S")
    six_pm = now.replace(hour=six_pm.time().hour, minute=six_pm.time().minute, \
        second=six_pm.time().second, microsecond=0)

    if now < mid_day:
        return sky_plus_strings.GOOD_MORNING
    elif now < six_pm:
        return sky_plus_strings.GOOD_AFTERNOON
    else:
        return sky_plus_strings.GOOD_EVENING

def traffic_light_is_red(frame):
    """Tell if the traffic light is red"""
    red_light = stbt.match(mysky_constants.TL_RED, frame=frame, region=mysky_constants.TRAFFIC_LIGHTS_REGION)
    return red_light

def traffic_light_is_yellow(frame):
    """Tell if the traffic light is yellow"""
    red_light = stbt.match(mysky_constants.TL_YELLOW, frame=frame, region=mysky_constants.TRAFFIC_LIGHTS_REGION)
    return red_light

def traffic_light_is_green(frame):
    """Tell if the traffic light is green"""
    red_light = stbt.match(mysky_constants.TL_GREEN, frame=frame, region=mysky_constants.TRAFFIC_LIGHTS_REGION)
    return red_light

def get_bottom_text_region(region):
    """Return the text area of a menu item"""
    text_region = Region(region.x + 8, region.bottom - 45, right=region.right - 6, bottom=region.bottom - 5)
    return text_region

def get_default_image_region(region):
    """Return the text area of a menu item"""
    text_region = Region(region.x + 8, region.y + 5, right=region.right - 6, bottom=region.bottom - 45)
    return text_region

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import stbt
from stbt import Region
import mysky_constants

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

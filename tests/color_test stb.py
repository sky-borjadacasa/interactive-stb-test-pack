#!/usr/bin/env python
"""
Test cases for MySky
"""

from time import sleep

import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region

class MySkyMainMenu(FrameObject):

    @property
    def is_visible(self):
        return stbt.match('images/SkyTopLogo.png', region=MY_SKY_REGION)

    @property
    def message(self):
        return 'message'

    @property
    def _info(self):
        return match('images/SkyTopLogo.png', frame=self._frame)

def test_get_yellow():
    """Open MySky app"""
    try:
        stbt.press('KEY_YELLOW')
        menu = stbt.wait_until(MySkyMainMenu)
        assert menu.is_visible
        print 'MySky menu is visible'
        
        sleep(10)

        greeting = menu.title
        print 'Greeting: {0}'.format(greeting)
        print 'Greeting string: {0}'.format(greeting_string())
        assert greeting == greeting_string()

        menu_items = menu.menu_items
        for item in menu_items:
            print 'Item text: {0}'.format(item.text)
            print 'Item selected: {0}'.format(item.selected)
        print len(menu_items)
        assert len(menu_items) == 3

        message = menu.message
        print 'Item message: {0}'.format(message)
        assert message == 'Find out more'

        return 0
    finally:
        clear_test()

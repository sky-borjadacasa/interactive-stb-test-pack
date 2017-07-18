#!/usr/bin/env python
"""
Test cases for MySky
"""
# Import util:
def install_and_import(package, package_name=None):
    """Function to install and import the needed packages.

    Args:
        pacakge (str): The name of the package to import
        package_name (str): Name of the pip package when it's not the same as the package name
    """
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        if package_name is not None:
            pip.main(['install', package_name])
        else:
            pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

import os
import importlib
import datetime
import stbt
from stbt import FrameObject, match, MatchParameters, ocr, Region
from time import sleep

os.system('sudo apt-get -y install python-scipy')
install_and_import('scipy.stats', 'scipy')
from scipy.stats import itemfreq

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

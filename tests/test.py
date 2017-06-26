#!/usr/bin/env python

import os
import pwd

def test_username():
	print 'Username: {0}'.format(pwd.getpwuid(os.getuid())[0])
	p = os.system('whoami')
	p = os.system('sudo whoami')
	p = os.system('sudo pip install opencv-python')
	p = os.system('sudo pip install numpy')
	p = os.system('sudo pip install tesserocr')
	p = os.system('sudo pip install pillow')
	p = os.system('sudo pip install matplotlib')
	p = os.system('sudo pip install scipy')
	p = os.system('sudo pip install fuzzyset')

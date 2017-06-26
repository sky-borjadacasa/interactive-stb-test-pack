#!/usr/bin/env python

import os
import pwd

def test_username():
    print 'Username: {0}'.format(pwd.getpwuid(os.getuid())[0])
    p = os.system('whoami')
    p = os.system('sudo whoami')

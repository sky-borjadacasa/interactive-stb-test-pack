#!/usr/bin/env python

import os
import pwd

def test_username():
    print pwd.getpwuid(os.getuid())[0]
#!/usr/bin/env python

import os
import pwd

def test_username():
	print 'Username: {0}'.format(pwd.getpwuid(os.getuid())[0])
	p = os.system('whoami')
	p = os.system('sudo whoami')
	p = os.system('sudo pip install opencv-python')
	p = os.system('sudo pip install numpy')
	p = os.system('sudo aptitude install tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev')
	p = os.system('pkg-config --cflags --libs tesseract')
	p = os.system('pwd')
	p = os.system('cat tesseract.pc')
	file_content = '''prefix=/usr
exec_prefix=${prefix}
bindir=${exec_prefix}/bin
datarootdir = ${prefix}/share
datadir=${datarootdir}
libdir=${exec_prefix}/lib
includedir=${prefix}/include/tesseract

Name: tesseract
Description: An OCR Engine that was developed at HP Labs between 1985 and 1995... and now at Google.
URL: https://code.google.com/p/tesseract-ocr
Version: 3.03
# Requires.private: lept
Libs: -L${libdir} -ltesseract
Libs.private: -lpthread -llept 
Cflags: -I${includedir}
'''
	text_file = open("/usr/lib/pkgconfig/tesseract.pc", "w")
	text_file.write(file_content)
	text_file.close()
	#p = os.system('sudo cp tesseract.pc /usr/lib/pkgconfig/tesseract.pc')
	#p = os.system('sudo pip install tesserocr')
	#p = os.system('sudo pip install pillow')
	#p = os.system('sudo pip install matplotlib')
	#p = os.system('sudo pip install scipy')
	#p = os.system('sudo pip install fuzzyset')

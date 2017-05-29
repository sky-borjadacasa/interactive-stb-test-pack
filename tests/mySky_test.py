from time import sleep

import stbt

def test_open_mysky():
	try:
		stbt.press('KEY_YELLOW')
		assert stbt.wait_for_match('mySky/SkyTopLogo.png')
		m = stbt.match_text("Good afternoon")
		assert m.match
		print stbt.ocr()
	finally:
		clear_test()

def clear_test():
	while stbt.wait_for_match('mySky/SkyTopLogo.png'):
		stbt.press('KEY_BACKUP')
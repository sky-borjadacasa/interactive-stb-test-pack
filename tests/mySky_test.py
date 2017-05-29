from time import sleep

import stbt

def test_open_mysky():
	stbt.press('KEY_YELLOW')
	assert stbt.wait_until(stbt.match_text('loading...'))
	assert stbt.wait_for_match('mySky/SkyTopLogo.png')
	print stbt.ocr()
	clear_test()

def clear_test():
	while stbt.wait_for_match('mySky/SkyTopLogo.png'):
		stbt.press('KEY_BACKUP')
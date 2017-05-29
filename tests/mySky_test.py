from time import sleep

import stbt

def test_open_mysky():
	stbt.press('KEY_YELLOW')
	assert stbt.wait_until(lambda: find_selection().text == "loading...")
	assert stbt.wait_for_match('mySky/SkyTopLogo.png')
	print stbt.ocr()
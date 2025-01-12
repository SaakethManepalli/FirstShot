import cv2
import numpy as np
import os
from Detectron2 import analyze_img


def pre_process_ss(filename):
    main_image = cv2.imread(f"/Users/saakethmanepalli/PycharmProjects/TeenHacks/uploads/{filename}")
    template_image = cv2.imread("/Users/saakethmanepalli/PycharmProjects/TeenHacks/uploads/ammo_img.png")

    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.80
    loc = np.where( result >= threshold)

    if len(loc[0])>0:
        analyze_img(filename)
    else:
        os.remove(f"/Users/saakethmanepalli/PycharmProjects/TeenHacks/uploads/{filename}")
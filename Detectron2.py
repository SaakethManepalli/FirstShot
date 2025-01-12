import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
import requests
import math

import numpy as np
import os, json, cv2, random

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg


def analyze_img(filename):
    img = cv2.imread(f"/Users/saakethmanepalli/PycharmProjects/TeenHacks/uploads/{filename}")
    height, width = img.shape[:2]

    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg.MODEL.WEIGHTS = "/Users/saakethmanepalli/PycharmProjects/TeenHacks/model_final.pth"
    cfg.MODEL.DEVICE = "cpu"

    predictor = DefaultPredictor(cfg)
    outputs = predictor(img)

def nearest_enemy(outputs, height, width):
    bboxes = outputs["instances"].pred_boxes
    if len(bboxes) > 0:
        nearest_enemy_distance = 999999
        final_x = 999999
        final_y = 999999

        for j, bbox in enumerate(bboxes):
            bbox = bbox.tolist()
            x1, y1, x2, y2 = [int(i) for i in bbox]
            enemy_distance = math.sqrt(pow((y1+(y2-y1)/2) - height/2, 2) + pow((x1+(x2-x1)/2) - width/2, 2))

            if enemy_distance < nearest_enemy_distance:
                nearest_enemy_distance = enemy_distance
                if (x1+(x2-x1)/2) > width/2 and (y1+(y2-y1)/2) > height/2:
                    final_x = (x2-x1)/2
                    final_y = (y2-y1)/2
                elif (x1+(x2-x1)/2) < width/2 and (y1+(y2-y1)/2) > height/2:
                    final_x = ((x2-x1)/2) * -1
                    final_y = (y2-y1)/2
                elif (x1+(x2-x1)/2) < width/2 and (y1+(y2-y1)/2) < height/2:
                    final_x = ((x2-x1)/2) * -1
                    final_y = ((y2-y1)/2) * -1
                else:
                    final_x = (x2-x1)/2
                    final_y = ((y2-y1)/2) * -1

        r = requests.post('https://9e90-192-160-130-62.ngrok-free.app/sendback',data={'x': final_x,'y': final_y})
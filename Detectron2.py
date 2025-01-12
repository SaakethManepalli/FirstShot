import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
import requests

import numpy as np
import os, json, cv2, random

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg


def analyze_img(filename):
    img = cv2.imread(f"/Users/saakethmanepalli/PycharmProjects/TeenHacks/uploads/{filename}")
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    outputs = predictor(img)

def nearest_enemy(outputs):


    r = requests.post('https://9e90-192-160-130-62.ngrok-free.app/sendback',data={x:outputs['instances'].pred_boxes[0].tensor[0][0],y:outputs['instances'].pred_boxes[0].tensor[0][1]})})
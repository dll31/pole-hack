# from torchvision.utils import draw_bounding_boxes
import torch
import pandas
import cv2
# import time
# import albumentations.pytorch
# from torchvision.models.detection import fasterrcnn_resnet50_fpn
# from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
# import numpy as np
import datetime
from DataStruct import Ds


class Predictor():
    def __init__(self, model_path, score_threshold, size):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        self.device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(self.device)
        self.model.conf = score_threshold
        self.size = size

    def analyze_box(self, max_side):
        if max_side < 40:
            return 6
        elif 40 <= max_side < 70:
            return 5
        elif 70 <= max_side < 80:
            return 4
        elif 80 <= max_side < 100:
            return 3
        elif 100 <= max_side < 150:
            return 2
        elif 150 <= max_side < 250:
            return 1
        else:
            return 0

    def visualize_bbox(self, img, bbox, color=(255, 0, 0), thickness=2):

        x_min, y_min, x_max, y_max = bbox
        x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)

        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)

        ((text_width, text_height), _) = cv2.getTextSize("Oversized", cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
        cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), (255, 0, 0), -1)
        cv2.putText(
            img,
            text="Oversized",
            org=(x_min, y_min - int(0.3 * text_height)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.35,
            color=(255, 255, 255),
            lineType=cv2.LINE_AA,
        )
        return img

    def __call__(self, image):
        result = self.model(image)
        result.render()

        counts = [0] * 7
        data = {str(i): counts[i] for i in range(7)}

        biggest = -1
        for box in result.pandas().xyxy[0].iterrows():
            x_min = box[1]['xmin']
            y_min = box[1]['ymin']
            width = box[1]['xmax'] - x_min
            height = box[1]['ymax'] - y_min
            max_side_size = max(width, height) * 2.67 # длина в миллиметрах
            counts[self.analyze_box(max_side_size)] += 1
            if max_side_size > biggest:
                biggest = max_side_size
            if max_side_size > self.size:
                result.ims[0] = self.visualize_bbox(result.ims[0], (x_min, y_min, box[1]['xmax'], box[1]['ymax']))

        data['time'] = datetime.datetime.now().strftime("%H:%M:%S")
        for i in range(7):
            data[str(i)] = counts[i]

        max_object = {'max_size': biggest,
                      'time': datetime.datetime.now().strftime("%H:%M:%S")
                     }
        return result.ims[0], data, max_object
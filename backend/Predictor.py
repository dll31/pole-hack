from torchvision.utils import draw_bounding_boxes
import torch
import albumentations.pytorch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import numpy as np


class Predictor():
    def __init__(self, model_path, score_threshold):
        self.model = fasterrcnn_resnet50_fpn(pretrained=False)
        in_features = self.model.roi_heads.box_predictor.cls_score.in_features
        num_classes = 2
        self.model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
        try:
            self.model.load_state_dict(torch.load(model_path))
            print("Модель успешно загружена")
        except:
            pass
        self.device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')

        self.model.eval()
        self.transforms = albumentations.Compose([
            albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            albumentations.pytorch.transforms.ToTensorV2()
            ])
        self.score_threshold = score_threshold

    def __call__(self, image):
        with torch.no_grad():
            img = self.transforms(image=image)['image'][None, ...].to(self.device)
            y_pred = self.model(img)
            # print(type(image), image.shape)
            img_boxed = draw_bounding_boxes(torch.Tensor(np.transpose(image, (2, 0, 1))).byte(),
                                            boxes=y_pred[0]['boxes'][y_pred[0]['scores'] > self.score_threshold],
                                            width=5)
            return img_boxed.numpy()
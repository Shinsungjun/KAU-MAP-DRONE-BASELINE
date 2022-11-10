from detect_model.model import DetectMultiBackend
from detect_model.data import letterbox
from detect_model.utils.general import non_max_suppression, scale_boxes
import torch
import cv2
import numpy as np

class DetectModel():
    def __init__(self) -> None:
        device = torch.device('cuda:0')
        weights = 'best.pt'
        self.model = DetectMultiBackend(weights, device=device, dnn=False, data=None, fp16=False)
        stride, names = self.model.stride, self.model.names
        self.conf_thres = 0.7
        self.iou_thres = 0.45
        self.classes = None
        self.agnostic_nms=False
        self.max_det= 5

    def detect(self, img_origin):
        '''
        input : img_origin - numpy image (HWC, BGR) resolution = (144, 256)
        output : detected box [n, 6] / dn : number of boxes / 6 : [x1, y1, x2, y2, precision, class] 
        '''
        #* Image Processing *#
        img = self.img_process(img_origin)

        #* Object Detection Model Inference *#
        pred = self.model(img, augment=False, visualize=False)

        #* NMS *#
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)

        #* Scale to Original Image size *#
        for i, det in enumerate(pred):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img_origin.shape).round()

        return det

    def img_process(self, img):
        im = letterbox(img, 640, stride=32, auto=True)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB -> Need to Fix
        im = np.ascontiguousarray(im)  # contiguous
        im = torch.from_numpy(im).to(self.model.device)
        im = im.float()
        im /= 255 # Normalize 0 ~ 1
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        return im



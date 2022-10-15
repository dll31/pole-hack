from DataStruct import DataStruct
from threading import Thread, Lock
from Predictor import Predictor
import torch
from grabThread import WebcamVideoStream
import numpy as np
import cv2
import time

locker = Lock()

class ModelThread:
    def __init__(self, vs):
        self.ds = DataStruct()
        self.stopped = False
        self.vs = vs
        self.pr = Predictor(model_path='model.zip', score_threshold=.6)
        self.locker = locker
        self.t = Thread(target=self.start_model, args=())
        self.flag = False

    def start_model(self):
        while True:
            if self.stopped:
                return
            self.locker.acquire()
            # self.ds.frame = self.vs.read()
            self.ds.frame = self.vs.read()
            self.ds.frame = self.pr(cv2.resize(self.ds.frame, (1080, 720)))
            self.flag = True

    def start(self):
        self.t.daemon = True
        self.t.start()
        return self

    def read(self):
        if self.ds.frame is not None:
            self.flag = False
            self.locker.release()
            return self.ds
        return None

    def stop(self):
        self.stopped = True
        self.vs.stop()
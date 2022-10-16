from threading import Thread, Lock
from Predictor import Predictor
from threading import BoundedSemaphore, Thread
import torch
from grabThread import WebcamVideoStream
import numpy as np
# import cv2
import time

locker = Lock()

class ModelThread:
    def __init__(self, vs, size):
        self.frame = None
        self.stopped = False
        self.vs = vs
        self.pr = Predictor(model_path='best.pt', score_threshold=.6, size=size)
        self.locker = locker
        self.t = Thread(target=self.start_model, args=())
        self.flag = False
        self.data = None
        self.max_object = None
        self.size = size

    def start_model(self):
        while True:
            if self.stopped:
                return
            self.locker.acquire()
            self.pr.size = self.size
            self.frame, self.data, self.max_object = self.pr(self.vs.read())
            self.flag = True

    def start(self):
        self.t.daemon = True
        self.t.start()
        return self

    def read(self):
        if self.frame is not None:
            self.flag = False
            self.locker.release()
            return self.frame, self.data, self.max_object
        return None

    def stop(self):
        self.stopped = True
        self.vs.stop()
from flask import Flask, Response, render_template, jsonify
import json
from datetime import datetime
import random
import cv2
import time
import DataStruct
from threading import Thread

class manager:
    def __init__(self, src=0):
        # current frame
        self.frame = None
        # current data
        self.json_data = None
        # stop signal
        self.stopped = False
        # Video Thread
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # Frame rate of Video
        self.frame_rate = None
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        if int(major_ver) < 3:
            self.frame_rate = self.stream.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            self.frame_rate = self.stream.get(cv2.CAP_PROP_FPS)

    def update(self, ds):
        while True:
            if self.stopped:
                return
            self.frame = ds.frame
            self.json_data = ds.json_data
            time.sleep(1 / (self.frame_rate + 13))

    def stop(self):
        self.stopped = True

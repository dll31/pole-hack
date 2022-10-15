import time
from threading import Thread, Lock
import cv2
from queue import Queue

locker = Lock()

class WebcamVideoStream:
    def __init__(self, src=0):
        self.locker = locker
        self.t = Thread(target=self.update, args=())
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # self.grabbed = False
        # self.frame = None
        # self.rc = False

        # self.que = Queue(200)

        self.grabbed, self.frame = self.stream.read()
        # initialize the variable used to indicate if the thread should
        self.framerate = None
        # be stopped
        self.stopped = False

        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        if int(major_ver) < 3:
            self.framerate = self.stream.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            self.framerate = self.stream.get(cv2.CAP_PROP_FPS)

    def start(self):
        self.t.daemon = True
        self.t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            # if not self.que.full():
            self.locker.acquire()
            self.grabbed, self.frame = self.stream.read()
            # time.sleep(1 / (self.framerate + 22))
            # 13 it is bruteforce value
            # if self.grabbed:
            #     self.que.put_nowait(self.frame)
            # else:
            #     self.stop()

    def read(self):
        if self.grabbed:
            self.locker.release()
            return self.frame
        return None
        # return self.que.get_nowait()

    def get_framerate(self):
        return self.framerate

    def stop(self):
        self.stopped = True


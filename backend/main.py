from flask import Flask, Response, render_template, jsonify, request
# import threading

import json
from datetime import datetime
import random
# import pandas as pd
# from DataStruct import DataStruct
from ModelThread import ModelThread
import cv2
# import matplotlib.pyplot as plt
# from numpy import array2string
from grabThread import WebcamVideoStream
import time


template_folder = 'templates'
app = Flask(__name__, template_folder=template_folder)
data = None
max_object = None
size = 30

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/query', methods=['POST'])
def get_query_from_react():
    _data = request.get_json()
    print(_data)
    return _data


def plot_data_gen():
    while True:
        time.sleep(0.1)
        json_data = json.dumps(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "value": random.random() * 100,
            }
        )
        return json_data


@app.route("/plot_data")
def plot_data():
    print(data)
    return json.dumps(data)


def plot_an_data_gen():
    while True:
        time.sleep(2)
        json_data = json.dumps(
            max_object
        )

        return json_data


@app.route("/plot_an_data")
def plot_an_data():
    print(max_object)
    return json.dumps(max_object)


def gen():
    global data, max_object
    vs = WebcamVideoStream(src='video.mp4').start()
    mt = ModelThread(vs=vs, size=size).start()
    # fps = vs.get_framerate()
    # print(fps)
    # time.sleep(0.1)
    # delay = 1 / fps


    while True:
        if mt.size != size:
            mt.size = size
        if mt.flag:
            frame, data, max_object = mt.read()
            if frame is not None:

                rc, frame = cv2.imencode('.jpg', frame)
                if rc:
                    yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n'
                else:
                    break
    mt.stop()


@app.route('/video_feed')
def video_feed():
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


# if __name__ == "__main__":
#     app.run(debug=True, use_debugger=True, use_reloader=False)

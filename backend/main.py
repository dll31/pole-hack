from flask import Flask, Response, render_template, jsonify, request
import threading
from grabThread import *
import json
from datetime import datetime
import random
from DataStruct import DataStruct
from ModelThread import ModelThread
import matplotlib.pyplot as plt
from numpy import array2string

template_folder = 'templates'
app = Flask(__name__, template_folder=template_folder)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/query', methods=['POST'])
def get_query_from_react():
    data = request.get_json()
    print(data)
    return data


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
    return plot_data_gen()


def plot_an_data_gen():
    while True:
        time.sleep(0.1)
        json_data = json.dumps(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "value": random.random() * 20,
            }
        )

        return json_data


@app.route("/plot_an_data")
def plot_an_data():
    return plot_an_data_gen()


@app.route("/plot_data")
def plot_data():
    json_data = json.dumps(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "value": random.random() * 100,
        }
    )
    return json_data


def gen():
    vs = WebcamVideoStream(src='video.mp4').start()
    mt = ModelThread(vs=vs).start()
    # fps = vs.get_framerate()
    # print(fps)
    # time.sleep(0.1)
    # delay = 1 / fps


    while True:
        if mt.flag:
            ds = mt.read()
            if ds.frame is not None:
                f = open('test.txt', 'a')
                f.write(array2string(ds.frame))
                f.close()
                rc, frame = cv2.imencode('.jpg', ds.frame)


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


if __name__ == "__main__":
    app.run(debug=True, use_debugger=True, use_reloader=False)

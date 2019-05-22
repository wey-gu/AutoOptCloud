import csv
import json
import numpy as np
import requests
import sys
import time

from flask import Flask, jsonify, request, g
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import emit, disconnect
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from ..config import Config


DATA_CSV_FOLDER_PATH = "/var/lib/cloud_pipeline"
DATA_CSV_PATH = DATA_CSV_FOLDER_PATH + "/data.csv"
BACKEND_ENDPOINT = "http://localhost:5000"
NORMALIZATION = {
    "rabbitmq": lambda x: np.divide(float(x), 1000),
    "fileio": lambda x: np.divide(float(x), 10),
    "mysql": lambda x: np.divide(float(x), 10),
    "iperf3": lambda x: np.multiply(float(x), 100),
    "cpu": lambda x: np.divide(float(x), 30),
    "benchmark": lambda x: np.divide(np.log(float(x)), 5)
}

HEADER_COLOR = {
    "rabbitmq": "green",
    "fileio": "yellow",
    "mysql": "orange",
    "iperf3": "red",
    "cpu": "teal",
    "benchmark": "blue",
    "w_ram": "red",
    "w_disk": "yellow",
    "w_user_p": "pink",
    "w_iowait_p": "blue",
    "w_frequency": "cyan",
    "w_idle_p": "green",
    "w_cpu_p": "orange",
    "w_kernel_p": "indigo",
}

LINE_COLOR = {
    "blue": "#2196F3",
    "green": "#00E676",
    "orange": "#FFAB40",
    "red": "#FF1744",
    "pink": "#F06292",
    "indigo": "#3D5AFE",
    "yellow": "#FFEA00",
    "teal": "#1DE9B6",
    "cyan": "#00838F"
}


BACKGRD_COLOR = {
    "blue": "#E3F2FD",
    "green": "#E8F5E9",
    "orange": "#FFF3E0",
    "red": "#FFCDD2",
    "pink": "#FCE4EC",
    "indigo": "#E8EAF6",
    "yellow": "#FFFDE7",
    "teal": "#E0F2F1",
    "cyan": "#E0F7FA"
}

BACKGRD_TRANS_COLOR = {
    "blue": "rgba(33, 150, 243, 0.1)",
    "green": "rgba(76, 175, 80, 0.1)",
    "orange": "rgba(255, 152, 0, 0.1)",
    "red": "rgba(244, 67, 54, 0.1)",
    "pink": "rgba(233, 30, 99, 0.1)",
    "indigo": "rgba(63, 81, 181, 0.1)",
    "yellow": "rgba(255, 235, 59, 0.1)",
    "teal": "rgba(0, 150, 136, 0.1)",
    "cyan": "rgba(0, 96, 100, 0.1)"
}

socketio = SocketIO()


def parse_data(path=DATA_CSV_PATH):
    dict_datas = list()
    handsontable_datas = list()
    charjs_datas = {
        "peformance": {},
        "weighers": {}
    }
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        handsontable_datas.append(headers)
        for row in reader:
            _row = preprocess_data(row)
            dict_datas.append(_row)
            handsontable_datas.append(list(_row.values()))
    headers_vuetify = [{
        "text": header,
        "value": header,
        "width": "6.2%",
    } for header in headers]
    # """
    # handsontableJS

    # ref: https://github.com/handsontable/vue-handsontable-official

    # example:
    # ['Year', 'Tesla', 'Mercedes', 'Toyota', 'Volvo'],
    # ['2019', 10, 11, 12, 13],
    # ['2020', 20, 11, 14, 13],
    # ['2021', 30, 15, 12, 13]
    # """
    # use np for better transposing performance
    data_2d_T = np.array(handsontable_datas[1:]).T

    # id as labels of the chartJS charts
    id_iterations = data_2d_T[0].tolist()  # for serilizaiton

    # benchmark, rabbitmq, fileio, mysql, iperf3, cpu
    perf_index = np.s_[1, 3:8]
    perf_headers = [headers[perf_index[0]]] + headers[perf_index[1]]
    perf_data = [data_2d_T[perf_index[0]].T.tolist()] + \
        [a for a in data_2d_T[perf_index[1]].tolist()]

    # w_ram, w_disk, w_user_p, w_iowait_p, w_frequency
    # w_idle_p, w_cpu_p, w_kernel_p
    weighers_index = np.s_[8:]
    weighers_headers = headers[weighers_index]
    weighers_data = data_2d_T[weighers_index].tolist()

    """
    chartJS

    ref: https://www.chartjs.org/samples/latest/charts/area/line-stacked.html

    data scheme chartjs handles:
    {
        "labels": ["January", "February", "March"],
        "datasets": [{
            "label": "My First dataset",
            "data": [
                1,
                2,
                3
            ]
        }, {
            "label": "My Second dataset",
            "data": [
                1,
                1,
                1

            ]
        }, {
            "label": "My Third dataset",
            "data": [
                1,
                1,
                1
            ]
        } ]
    }
    """

    charjs_datas["peformance"] = {
        "labels": id_iterations,
        "datasets": [
            {
                "label": header, "data": perf_data[i], "borderWidth": 1,
                "pointBackgroundColor": "white", "pointBorderColor": "white",
                "borderColor": LINE_COLOR[HEADER_COLOR[header]],
                "backgroundColor": BACKGRD_TRANS_COLOR[HEADER_COLOR[header]]
            }
            for i, header in enumerate(perf_headers)
        ]
    }

    charjs_datas["weighers"] = {
        "labels": id_iterations,
        "datasets": [
            {
                "label": header.split("w_")[1], "data": weighers_data[i], "borderWidth": 1,
                "pointBackgroundColor": "white", "pointBorderColor": "white",
                "borderColor": LINE_COLOR[HEADER_COLOR[header]],
                "backgroundColor": BACKGRD_TRANS_COLOR[HEADER_COLOR[header]]
            }
            for i, header in enumerate(weighers_headers)
        ]
    }

    max_benchmark = max(perf_data[0])
    max_benchmark_index = id_iterations[(
        [index for index, bench in enumerate(
            perf_data[0]) if bench == max_benchmark][0]
    )]

    return {
        "table_datas": dict_datas,
        # "handsontable_datas": handsontable_datas,
        "charjs_datas": charjs_datas,
        "max_benchmark": max_benchmark,
        "max_benchmark_index": max_benchmark_index,
        "headers": headers_vuetify,
    }


def create_data_watchdog_instance(path=DATA_CSV_FOLDER_PATH):

    event_handler = FileMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def update_data_POST(data, url=BACKEND_ENDPOINT + "/data"):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    # serilization
    data = json.dumps(data)
    r = requests.post(url, data=data, headers=headers)


def preprocess_data(row):
    """
    Preprocessing data
    - normalizing for better visualization
    - formatting for serilization
    """
    for key in row:
        value = row[key]
        if key in NORMALIZATION:
            row[key] = NORMALIZATION[key](value)
        elif key != "timestamp" and key != "id":
            row[key] = float(value)
        elif key == "id":
            row[key] = int(value)
    return row


class FileMonitor(PatternMatchingEventHandler):
    def on_modified(self, event):
        patterns = ["*/data.csv"]
        super(FileMonitor, self).on_modified(event)
        data = parse_data()
        update_data_POST(data)


def create_backend_instance(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db = json.dumps(parse_data())

    # socketio instantiation
    socketio.init_app(app)
    # enable CORS
    CORS(app)

    # http server
    @app.before_request
    def before_request():
        if 'db' not in g:
            g.db = db

    @app.route("/data", methods=["GET", "POST"])
    def data():
        """ get and post all data """
        if request.method == "GET":
            return jsonify(g.db)
        if request.method == "POST":
            db = request.get_json()
            try:
                socketio.emit("updateData", db, broadcast=True)
                return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}
            except:  # NOQA
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    return app

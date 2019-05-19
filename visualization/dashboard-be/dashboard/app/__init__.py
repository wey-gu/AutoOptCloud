import csv
import json
import numpy as np
import requests
import sys
import time

from flask import Flask, jsonify, request   
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import emit, disconnect
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

DATA_CSV_PATH = "/var/lib/cloud_pipeline/data.csv"
BACKEND_ENDPOINT = "http://localhost:8080"
NORMALIZATION = {
    "rabbitmq": lambda x: np.divide(float(x), 1000),
    "fileio": lambda x: np.divide(float(x), 10),
    "mysql": lambda x: np.divide(float(x), 10),
    "iperf3": lambda x: np.multiply(float(x), 100),
    "cpu": lambda x: np.divide(float(x), 10),
    "benchmark": lambda x: np.divide(np.log(float(x)), 5)
}

def create_backend_instance():
    app = Flask(__name__)
    socketio = SocketIO()
    DB = json.dumps(parse_data()) # closure as memory database

    # socketio instantiation
    socketio.init_app(app)
    # enable CORS
    CORS(app)

    # http server
    @app.route("/data", methods=["GET", "POST"])
    def data(DB):
        """ get and post all data """
        if request.method == "GET":
            return jsonify(DB)
        if request.method == "POST":
            DB = request.get_json()
            emit("updatedata", DB, broadcast=True)


def create_data_watchdog_instance(path=DATA_CSV_PATH):

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


def parse_data(path=DATA_CSV_PATH):
    # dict_datas = list()
    handsontable_datas = list()
    charjs_datas = {
        "peformance" : {},
        "weighers" : {}
        }
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        handsontable_datas.append(headers)
        for row in reader:
            _row = preprocess_data(row)
            # dict_datas.append(_row)
            handsontable_datas.append(list(_row.values()))

    """
    handsontableJS

    ref: https://github.com/handsontable/vue-handsontable-official

    example:
    ['Year', 'Tesla', 'Mercedes', 'Toyota', 'Volvo'],
    ['2019', 10, 11, 12, 13],
    ['2020', 20, 11, 14, 13],
    ['2021', 30, 15, 12, 13]
    """
    # use np for better transposing performance
    data_2d_T = np.array(handsontable_datas[1:]).T

    # id as labels of the chartJS charts
    id_iterations = data_2d_T[0].tolist() # for serilizaiton

    # benchmark, rabbitmq, fileio, mysql, iperf3, cpu
    perf_index = np.s_[1, 3:8]
    perf_headers = [headers[perf_index[0]]] + headers[perf_index[1]]
    perf_data = [data_2d_T[perf_index[0]].T.tolist()] + [ a for a in
        data_2d_T[perf_index[1]].tolist()
        ]

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
            {"label" : header, "data": perf_data[i]}
            for i, header in enumerate(perf_headers)
        ]
    }

    charjs_datas["weighers"] = {
        "labels": id_iterations,
        "datasets": [
            {"label" : header, "data": weighers_data[i]}
            for i, header in enumerate(weighers_headers)
        ]
    }

    return {
        # "dict_datas" : dict_datas,
        "handsontable_datas" : handsontable_datas,
        "charjs_datas" : charjs_datas,
        }


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


class FileMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        super(FileMonitor, self).on_modified(event)
        data = parse_data()
        update_data_POST(data)

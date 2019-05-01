import csv
import operator
import os
import numpy
import subprocess
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ..utils.h_client import Heatclient
from ..config import VNF_STACK_NAME, WORKING_DIR, ARG_KEYS, PLAYBOOK_FETCHDATA


INVENTORY_PATH = WORKING_DIR + "ansible_hosts"
DATA_LOG_PATH = WORKING_DIR + "dataLog/"
DB_CSV_PATH = WORKING_DIR + "data.csv"

BENCHMARK_NAMES = [
    "rabbitmq",
    "fileio",
    "mysql",
    "iperf3",
    "cpu"]
DB_CSV_NEW_COLUMNS = [
    "benchmark",
    "id"] + BENCHMARK_NAMES

DB_CSV_HEADER = ARG_KEYS + DB_CSV_NEW_COLUMNS

REMOTE_DATA_PATH = WORKING_DIR + "results/"
RABBIT_MQ_LOG = "rabbitmq.log"
FILEIO_LOG = "fileio.log"
MYSQL_LOG = "mysql.log"
IPERF_LOG = "iperf_c.log"
CPU_LOG = "cpu.log"


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.task_ok = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()] = result


class DataCollector:
    def __init__(self, args):
        if self.csv_db_missing():
            self.create_csv_db()
            self.data_record = args
            self.new_id = 0
        else:
            # tail -1 /path/to/data.csv
            # then increment the id
            lastRow = subprocess.check_output(
                ["tail", "-1", DB_CSV_PATH]
            )
            self.new_id = int(lastRow.split(",")[-1]) + 1
        self.data_path = DATA_LOG_PATH + str(self.new_id) + "/"
        # create data path
        subprocess.check_call(["mkdir", "-p", self.data_path])

    def setup_ansible(self):
        heat = Heatclient()
        ansible_hosts = heat.client.resources.get(
            VNF_STACK_NAME, "ansible_hosts").attributes["value"]
        inventory_string = "[VM]\n" + ansible_hosts + "\n"
        with open(INVENTORY_PATH, "w") as inventory_file:
            inventory_file.write(inventory_string)

    def fetch_files(self):
        """
        Fetch files from all hosts via ansible playbook

        reference:
          https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html
        """
        loader = DataLoader()
        with open(INVENTORY_PATH, "r") as inventory_file:
            inventory = InventoryManager(
                loader=loader,
                sources=inventory_file.read()
            )

        variable_manager = VariableManager(
            loader=loader,
            inventory=inventory,
        )

        variable_manager.extra_vars = {
            "data_id": self.new_id,
            "data_path": self.data_path,
            "remote_path": REMOTE_DATA_PATH
        }

        playbook = PlaybookExecutor(
            playbooks=[PLAYBOOK_FETCHDATA],
            inventory=inventory,
            loader=loader,
            variable_manager=variable_manager
        )
        results_callback = ResultCallback()
        playbook._tqm._stdout_callback = results_callback
        playbook.run()

    def parse_data(self):
        self.benchmarkList = [
            self.benchmark_rabbitmq(),
            self.benchmark_fileio(),
            self.benchmark_mysql(),
            self.benchmark_iperf(),
            self.benchmark_cpu()
        ]
        self.benchmark = numpy.prod(self.benchmarkList)

    def collect(self):
        self.setup_ansible()
        self.fetch_files()
        self.parse_data()
        benchmark_data_record = dict(zip(
            DB_CSV_NEW_COLUMNS,
            [
                self.benchmark,
                self.new_id,
            ] + self.benchmarkList
        ))
        self.data.update(benchmark_data_record)
        self.insert_row_db()

    @property
    def get_benchmark(self):
        return self.benchmark

    def benchmark_rabbitmq(self):
        data_path = self.data_path + RABBIT_MQ_LOG
        recieveRateAvgRow = subprocess.check_output(
            " ".join(
                ["grep", "'receiving rate avg'", data_path,
                 "|", "tail", "-1"]),
            shell=True
        )
        self.rabbit_id, self.rabbit_rate = operator.itemgetter(
            1, -2)(recieveRateAvgRow.split())
        consumerLatencylines = subprocess.check_output(
            " ".join(
                ["grep", self.rabbit_id, data_path, "|",
                 "grep", "'consumer latency'"]),
            shell=True
        ).split("\n")
        consumerLatency = [int(line.split(
            "/")[-2]) for line in consumerLatencylines]
        consumerLatency_mean_ms = sum(
            consumerLatency) * 0.001 / len(consumerLatency)
        self.rabbit_bm = float(self.rabbit_rate) * consumerLatency_mean_ms
        return self.rabbit_bm

    def benchmark_fileio(self):
        data_path = self.data_path + FILEIO_LOG
        fileiolines = subprocess.check_output(
            " ".join(
                ["grep", "Throughput", data_path, "-A", "12",
                 "|", "tail", "-n", "12"]),
            shell=True).split("\n")
        self.fileio_read = float(fileiolines[0].split()[-1])
        self.fileio_write = float(fileiolines[1].split()[-1])
        self.fileio_latency = float(fileiolines[-2].split()[-1])
        self.fileio_bm = (
            self.fileio_read * self.fileio_write / self.fileio_latency)
        return self.fileio_bm

    def benchmark_mysql(self):
        data_path = self.data_path + MYSQL_LOG
        mysqllines = subprocess.check_output(
            " ".join(["grep", "transactions", data_path, "-A", "13",
                      "|", "tail", "-n", "13"]),
            shell=True).split("\n")
        self.mysql_trans = float(mysqllines[0].split()[2].split("(")[1])
        self.mysql_latency = float(mysqllines[-2].split()[-1])
        self.mysql_bm = (
            self.mysql_trans / self.mysql_latency)
        return self.mysql_bm

    def benchmark_cpu(self):
        data_path = self.data_path + CPU_LOG
        cpulines = subprocess.check_output(
            " ".join(["grep", "CPU", data_path, "-A", "9",
                      "|", "tail", "-n", "9"]),
            shell=True).split("\n")
        self.cpu_speed = float(cpulines[0].split()[-1])
        self.cpu_latency = float(cpulines[-2].split()[-1])
        self.cpu_bm = (
            self.cpu_speed / self.cpu_latency)
        return self.cpu_bm

    def benchmark_iperf(self):
        data_path = self.data_path + IPERF_LOG
        iperflines = subprocess.check_output(
            " ".join(["grep", "0.00-60.00", data_path,
                      "|", "grep", "sender",
                      "|", "tail", "-n", "1"]),
            shell=True).split("\n")
        self.iperf_bandwidth_Gbps = float(iperflines[-2].split()[5])
        self.iperf_retry = float(iperflines[-2].split()[7])
        self.iperf_bm = (
            self.iperf_bandwidth_Gbps * 1024 / self.iperf_retry)
        return self.iperf_bm

    def create_csv_db(self):
        with open(DB_CSV_PATH, "a") as db:
            writer = csv.DictWriter(db, DB_CSV_HEADER)
            writer.writeheader()

    def insert_row_db(self):
        with open(DB_CSV_PATH, "a") as db:
            writer = csv.DictWriter(db, DB_CSV_HEADER)
            writer.writerow(self.data_record)

    def csv_db_missing(self):
        return os.path.isfile(DB_CSV_PATH)

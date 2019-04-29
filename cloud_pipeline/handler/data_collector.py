import csv
import os
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
DB_CSV_NEW_COLUMN = [
    "benchmark",
    "id"]
DB_CSV_HEADER = ARG_KEYS + DB_CSV_NEW_COLUMN
REMOTE_DATA_PATH = WORKING_DIR + "results/"


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.task_ok = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()] = result


results_callback = ResultCallback()


class DataCollector:
    def __init__(self, args):
        if self.csv_db_missing():
            self.create_csv_db()
            self.data = args
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
        playbook._tqm._stdout_callback = results_callback
        playbook.run()

    def parse_data(self):
        pass

    def create_csv_db(self):
        with open(DB_CSV_PATH, "a") as db:
            writer = csv.DictWriter(db, DB_CSV_HEADER)
            writer.writeheader()

    def insert_row_db(self):
        with open(DB_CSV_PATH, "a") as db:
            writer = csv.DictWriter(db, DB_CSV_HEADER)
            writer.writerow(self.data)

    def csv_db_missing(self):
        return os.path.isfile(DB_CSV_PATH)

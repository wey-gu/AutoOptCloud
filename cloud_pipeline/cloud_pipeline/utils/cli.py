import sys
from subprocess import check_call
from cloud_pipeline import CloudPipeline
from cloud_pipeline.utils.h_client import Heatclient
from cloud_pipeline.utils.logger import LOG_FOLDER
from cloud_pipeline.config import VNF_HOT_PATH, VNF_ENV_PATH, VNF_STACK_NAME


cli_help_string = """
usage: cloudp <subcommand> [...]

\033[95m
Command-line interface to the Cloud Pipeline.
\033[0m

Sub Commands:
  log               Monitoring cloud pipeline logs
  stack             Monitoring VNF events
  load_gen          Load generation
  load_clean        Load cleanup
  vnf_create        VNF create
  vnf_clean         VNF cleanup
  get_bench [id]    Get latest benchmark
"""

subcommands = {
    "log": "Monitoring cloud pipeline logs",
    "stack": "Monitoring VNF events",
    "load_gen": "Load generation",
    "load_clean": "Load cleanup",
    "vnf_create": "VNF create",
    "vnf_clean": "VNF cleanup",
    "get_bench": "Get benchmark per id"
}

class bcolors():
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def main():
    args = sys.argv[1:]
    try:
        arg_validator(args)
        if args[0] == "log":
            check_call("lnav %s" % (LOG_FOLDER), shell=True)
        if args[0] == "stack":
            check_call(
                ". /root/openrc; openstack stack event list "
                "--nested-depth 6 vnf_benchmark_stack --follow "
                "| lnav", shell=True)
        if args[0] in ["-h", "--help"]:
            cli_help()
        if args[0] == "load_gen":
            cp = CloudPipeline()
            if not cp.load_existed():
                cp.load_gen()
        if args[0] == "load_clean":
            cp = CloudPipeline()
            if cp.load_existed():
                cp.load_cleanup()
        if args[0] == "vnf_create":
            heat = Heatclient()
            stack = heat.stack_create(
                hc=heat.client,
                HOT_path=VNF_HOT_PATH,
                env_path=VNF_ENV_PATH,
                stack_name=VNF_STACK_NAME
                )
        if args[0] == "vnf_clean":
            cp = CloudPipeline()
            if cp.vnf_existed():
                cp.vnf_cleanup()
        if args[0] == "get_bench":
            from cloud_pipeline.handler.data_collector import DataCollector
            from cloud_pipeline.config import ARG_KEYS
            import numpy as np
            # generate a random argument list
            randomeArgList = np.random.uniform(
                low=-1.0, high=1.0, size=(len(ARG_KEYS),))

            # build argument dict
            arg = dict(zip(ARG_KEYS, randomeArgList))
            try:
                new_id = args[1]
            except IndexError:
                new_id = 65535
                print(
                    bcolors.WARNING + "WARNING: " + bcolors.ENDC +
                    "id missing," +
                    "id: 65535 was mocked in this query for testing..."
                )
            data_collector = DataCollector(
                arg, ansible_stdout=True, new_id=int(new_id))
            try:
                print(
                    bcolors.OKGREEN + "INFO:" + bcolors.ENDC +
                    "\nProcessing started..."
                )
                data_collector.parse_data()
                print(
                    bcolors.OKGREEN + "INFO:" + bcolors.ENDC +
                    "\nProcessing finished...\n    Benchmark: " +
                    bcolors.OKBLUE +
                    str(data_collector.benchmark) +
                    bcolors.ENDC
                )
            except Exception as e:
                print(
                    bcolors.FAIL + "ERROR:" + bcolors.ENDC +
                    "\nget_bench failed: " +
                    str(e)
                )
        else:
            cli_help()
    except AssertionError:
        cli_help()


def arg_validator(args):
    """argument validator"""
    assert len(args) > 0, "No Sub Commands given"
    assert args[0] in subcommands.keys(), "ERROR: unknown subcommands %s" % args[1]


def cli_help():
    print(cli_help_string)
    print(
        bcolors.FAIL + "ERROR:" + bcolors.ENDC +
        "\nInvalid argument"
    )
if __name__ == '__main__':
    main()

import sys
from subprocess import check_call
from cloud_pipeline import CloudPipeline
from cloud_pipeline.utils.h_client import Heatclient
from cloud_pipeline.utils.logger import LOG_FOLDER
from cloud_pipeline.config import VNF_HOT_PATH, VNF_ENV_PATH, VNF_STACK_NAME


cli_help_string = """
usage: cloudp

Commands:
  log               Monitoring cloud pipeline logs
  stack             Monitoring VNF events
  load_gen          Load generation
  load_clean        Load cleanup
  vnf_create        VNF create
  vnf_clean         VNF cleanup
  get_bench [id]    Get latest benchmark

"""

def main():
    args = sys.argv[1:]
    try:
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
                print("Warning: id missing, id:65535 mocked in this query for testing...")
            data_collector = DataCollector(arg, ansible_stdout=True, new_id=int(new_id))
            try:
                print("Processing started...")
                data_collector.parse_data()
                print("Processing finished...\n    Benchmark: " + str(data_collector.benchmark))
            except Exception as e:
                print("get_bench failed: %s" % (str(e)))

    except Exception as e:
        cli_help()

def arg_validator(args):
    """tobedone"""
    pass

def cli_help():
    print(cli_help_string)
if __name__ == '__main__':
    main()

import sys
from subprocess import check_call
from .. import CloudPipeline
from .utils.h_client import Heatclient
from .utils.logger import LOG_FOLDER
from ...config import VNF_HOT_PATH, VNF_ENV_PATH, VNF_STACK_NAME


cli_help_string = """
usage: cloudp

Commands:
  log            Monitoring cloud pipeline logs
  stack          Monitoring VNF events
  load_gen       Load generation
  load_clean     Load generation
  vnf_create     VNF create

"""

def main():
    args = sys.argv[1:]
    try:
        if args[0] == "log":
            check_call("lnav %s" % (LOG_FOLDER), shell=True)
        if args[0] == "stack":
            check_call(
                ". /root/openrc; openstack stack create --template vnf.yaml "
                "--environment envFiles/vnf_env.yaml "
                "--wait vnf_benchmark_stack", shell=True)
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
    except Exception as e:
        cli_help()

def cli_help():
    print(cli_help_string)
if __name__ == '__main__':
    main()
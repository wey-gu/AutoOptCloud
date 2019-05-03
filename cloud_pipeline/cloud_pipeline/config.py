OS_TENANT_NAME = "admin"
OS_USERNAME = "admin"
OS_PASSWORD = "admin"
OS_AUTH_URL = "http://192.168.2.28:5000/v2.0"
OS_CACERT = "/path/to/certs/OS-ca.crt"

# VNF for benchmark
VNF_STACK_NAME = "vnf_benchmark_stack"
VNF_HOT_PATH = "resources/templates/vnf.yaml"
VNF_ENV_PATH = "resources/templates/envFiles/vnf_env.yaml"
VNF_CREATE_RETRY = 3
VNF_DELETE_RETRY = 3
# LOAD GENERATION ENV
LOADGEN_STACK_NAME = "load_generation_stack"
LOADGEN_HOT_PATH = "resources/templates/load_gen.yaml"
LOADGEN_ENV_PATH = "resources/templates/envFiles/load_gen_env.yaml"
LOADGEN_CREATE_RETRY = 3
LOADGEN_DELETE_RETRY = 3

APPLY_CONF_TEMPLATE_PATH = "resources/scripts/apply_config.pp"

ARG_KEYS = [
    "w_ram",
    "w_disk",
    "w_user_p",
    "w_iowait_p",
    "w_frequency",
    "w_idle_p",
    "w_cpu_p",
    "w_kernel_p"]

# data collection and VM benchmark path
WORKING_DIR = "/var/lib/cloud_pipeline/"
PLAYBOOK_FETCHDATA = "resources/ansible/playbooks/fetch-data.yaml"
COLLECTION_RETRY = 3

# benchmark_run
BENCHMARK_RUN_RETRY = 10

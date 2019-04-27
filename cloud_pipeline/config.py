OS_NO_CACHE = 'true'
OS_TENANT_NAME = 'admin'
OS_PROJECT_NAME = 'admin'
OS_USERNAME = 'admin'
OS_PASSWORD = 'admin'
OS_AUTH_URL = 'http://192.168.2.34:5000/v2.0'
OS_DEFAULT_DOMAIN = 'default'
OS_AUTH_STRATEGY = 'keystone'
OS_REGION_NAME = 'RegionOne'
CINDER_ENDPOINT_TYPE = 'internalURL'
GLANCE_ENDPOINT_TYPE = 'internalURL'
KEYSTONE_ENDPOINT_TYPE = 'internalURL'
NOVA_ENDPOINT_TYPE = 'internalURL'
NEUTRON_ENDPOINT_TYPE = 'internalURL'
OS_ENDPOINT_TYPE = 'internalURL'
OS_CACERT = '/path/to/certs/OS-ca.crt'

# VNF for benchmark
VNF_STACK_NAME = "vnf_benchmark_stack"
VNF_HOT_PATH = "resources/templates/vnf.yaml"
VNF_ENV_PATH = "resources/templates/envFiles/vnf_env.yaml"
VNF_CREATE_RETRY = 3
VNF_DELETE_RETRY = 3
# LOAD GENERATION ENV
LOAD_STACKNAME = "load_generation_stack"
LOADGEN_HOT_PATH = "resources/templates/load_gen.yaml"
LOADGEN_ENV_PATH = "resources/templates/envFiles/load_gen_env.yaml"

OS_credential = dict()
OS_credential["OS_TENANT_NAME"] = OS_TENANT_NAME
OS_credential["OS_USERNAME"] = OS_USERNAME
OS_credential["OS_PASSWORD"] = OS_PASSWORD
OS_credential["OS_AUTH_URL"] = OS_AUTH_URL
OS_credential["OS_CACERT"] = OS_CACERT

APPLY_CONF_TEMPLATE_PATH = 'resources/scripts/apply_config.pp'

ARG_KEYS = [
    "w_disk",
    "w_io_ops",
    "w_user_percent",
    "w_user_p",
    "w_iowait_p",
    "w_frequency",
    "w_idle_p",
    "w_p",
    "w_kernel_p"]

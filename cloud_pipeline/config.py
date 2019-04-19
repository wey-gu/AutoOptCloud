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

LOAD_STACKNAME = "load_generation_stack"

OS_credential = dict()
OS_credential["OS_TENANT_NAME"] = OS_TENANT_NAME
OS_credential["OS_USERNAME"] = OS_USERNAME
OS_credential["OS_PASSWORD"] = OS_PASSWORD
OS_credential["OS_AUTH_URL"] = OS_AUTH_URL
OS_credential["OS_CACERT"] = OS_CACERT

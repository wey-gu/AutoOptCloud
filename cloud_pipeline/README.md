## API reference

### cloud_pipeline

```python

from cloud_pipeline import CloudPipeline
from cloud_pipeline.config import ARG_KEYS
import numpy as np


# instantiate cloud_pipeline
cp = CloudPipeline()

# genarate load
load_gen = cp.load_gen()

# wait for a while
import time
time.sleep(5*60)

# generate a random argument list
randomeArgList = np.random.uniform(low=-1.0, high=1.0, size=(len(ARG_KEYS),))

# build argument dict
arg = dict(zip(ARG_KEYS, randomeArgList))

# query a benchmark

benchmark = cp.benchmark_run(arg)

```

> test notes to be transferred to unit tests

## manually create load-gen resources

```bash
cd /var/lib/cloud_pipeline/cloud_pipeline/resources/templates
openstack stack create --template load_gen.yaml --environment  envFiles/load_gen_env.yaml  --wait load_generation_stack
```

## manually query a benchmark

```bash
cd /var/lib/cloud_pipeline/cloud_pipeline/resources/templates
openstack stack create --template vnf.yaml --environment  envFiles/vnf_env.yaml  --wait vnf_benchmark_stack
```

## manually test

### create a benchmark VNF

> Test utils

```python

from cloud_pipeline.utils.h_client import Heatclient
from cloud_pipeline.config import VNF_HOT_PATH, VNF_ENV_PATH, VNF_STACK_NAME

heat = Heatclient()
stack = heat.stack_create(
    hc=heat.client,
    HOT_path=VNF_HOT_PATH,
    env_path=VNF_ENV_PATH,
    stack_name=VNF_STACK_NAME
    )

```

> Test handler

```python
from cloud_pipeline.handler.vnf_handler import VnfHandler

vnf = VnfHandler()
vnf.create_vnf()
```

### collect data

> manually test anisble only

```bash
cd /var/lib/cloud_pipeline/

cat <<EOF > extra_var.json
{
    "data_id": "1024",
    "data_path": "/var/lib/cloud_pipeline/dataLog/1024/",
    "remote_path": "/var/lib/cloud_pipeline/results/"
}
EOF
ANSIBLE_HOST_KEY_CHECKING=False \
    ansible-playbook --inventory-file /var/lib/cloud_pipeline/ansible_hosts \
        --extra-vars @/var/lib/cloud_pipeline/extra_var.json \
        /var/lib/cloud_pipeline/cloud_pipeline/resources/ansible/playbooks/fetch-data.yaml

```

```python
from cloud_pipeline.handler.data_collector import DataCollector
from cloud_pipeline.config import ARG_KEYS
import numpy as np
# generate a random argument list
randomeArgList = np.random.uniform(low=-1.0, high=1.0, size=(len(ARG_KEYS),))

# build argument dict
arg = dict(zip(ARG_KEYS, randomeArgList))
data_collector = DataCollector(arg, ansible_stdout=True)

# ansible only
data_collector.fetch_files()

# parse log only
data_collector.parse_data()

```

> test DataCollector

```python
data_collector.collect()
data_collector.get_benchmark

```

## reference

https://docs.openstack.org/heat/latest/template_guide/hot_spec.html

https://docs.openstack.org/heat/latest/template_guide/openstack.html

https://developer.openstack.org/api-ref/orchestration/v1/index.html?expanded=create-stack-detail#stacks

## pre-requirement

patch on heatclient is needed: https://review.opendev.org/#/c/220921/4/heatclient/common/http.py

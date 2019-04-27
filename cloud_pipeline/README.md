
## manually create load-gen resources

```bash
openstack stack create --template load_gen.yaml --environment  envFiles/load_gen_env.yaml  --wait test-load-generation
```

## manually query a benchmark

```bash
openstack stack create --template vnf.yaml --environment  envFiles/vnf_env.yaml  --wait test-vnf-benchmark 
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

## reference

https://docs.openstack.org/heat/latest/template_guide/hot_spec.html
https://docs.openstack.org/heat/latest/template_guide/openstack.html
https://developer.openstack.org/api-ref/orchestration/v1/index.html?expanded=create-stack-detail#stacks


## pre-requirement

patch on heatclient is needed: https://review.opendev.org/#/c/220921/4/heatclient/common/http.py

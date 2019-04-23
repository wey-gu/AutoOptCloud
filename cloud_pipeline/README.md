
## manually create load-gen resources

```bash
openstack stack create --template load_generation.yaml --environment  envFiles/load_gen_env.yaml  --wait test-load-generation
```

## manually query a benchmark

```bash
openstack stack create --template vnf.yaml --environment  envFiles/vnf_env.yaml  --wait test-vnf-benchmark 
```

## reference

https://docs.openstack.org/heat/latest/template_guide/hot_spec.html
https://docs.openstack.org/heat/latest/template_guide/openstack.html
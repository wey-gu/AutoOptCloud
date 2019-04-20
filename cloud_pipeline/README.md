
## verify resources

```bash
openstack stack create --template load_generation.yaml --environment  envFiles/load_gen_env.yaml  --wait test-load-generation
```
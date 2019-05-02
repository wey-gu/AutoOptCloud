
## envrionment for dev on CEE

### virtualenv

```bash
python -m virtualenv --system-site-packages env
source env/bin/activate
```

### Package versions note:
> for jupyter on ubuntu 14.04, python 2.7.6
```
ipykernel==4.10.0
tornado==4.5.3
jupyter-client==5.2.4
jupyter==1.0.0
jupyter-console==5.2.0
jupyter-core==4.4.0
```

### jupyter note

```bash
source env/bin/activate
jupyter notebook --port 8080 --ip <IP_public> --allow-root
```

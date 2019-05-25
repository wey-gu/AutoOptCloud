## setup envrionment on CEE

```bash
mkdir -p /var/lib/cloud_pipeline

nova aggregate-create infra infra

nova aggregate-add-host compute-0-12.domain.tld infra

nova aggregate-create machineLearning machineLearning

nova aggregate-add-host machineLearning compute-0-8.domain.tld
nova aggregate-add-host machineLearning compute-0-9.domain.tld
nova aggregate-add-host machineLearning compute-0-10.domain.tld
nova aggregate-add-host machineLearning compute-0-11.domain.tld


nova flavor-delete 040436
nova flavor-create U04-RAM04-DISK-36 040436 4096 36 04
nova flavor-key 040436 set hw:mem_page_size=1048576
nova flavor-list --ext

nova flavor-delete 121264
nova flavor-create U14-RAM12-DISK-64 121264 12288 64 14
nova flavor-key 121264 set hw:mem_page_size=1048576
nova flavor-key 121264 set hw:cpu_policy=shared
nova flavor-delete 061264
nova flavor-create U06-RAM12-DISK-64 061264 12288 64 06
nova flavor-key 061264 set hw:mem_page_size=1048576
nova flavor-key 061264 set hw:cpu_policy=shared
nova flavor-list --ext

# patch heatclient
cp /var/lib/cloud_pipeline/packages/heatclient_common_http.py /usr/lib/python2.7/dist-packages/heatclient/common/http.py

# install python-dev
apt-get install python-dev --yes
```

> edit config.py for credneitials

```bash
vim /var/lib/cloud_pipeline/env/lib/python2.7/site-packages/cloud_pipeline/config.py

#OS_AUTH_URL = "<>"
#OS_CACERT = "<>"
```

> start jupyter

```bash
screen -S jupyter
source /var/lib/cloud_pipeline/env/bin/activate
jupyter notebook --ip <public_ip> --port 8080 --allow-root

^-ad
```



## Docker

```bash
apt-get install -y --force-yes docker.io cgroup-bin

docker load < opt-cloud_dockerImage.tar
docker load < opt-cloud_dockerImage_py2.tar

$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
<none>              <none>              8152b07f5c7f        16 minutes ago      1.101 GB
<none>              <none>              836a0d092e24        18 hours ago        1.155 GB

docker run -v /var/lib/cloud_pipeline:/var/lib/cloud_pipeline \
  -v /etc/localtime:/etc/localtime \
  -v /path/to/certs/OS-ca.crt:/path/to/certs/OS-ca.crt \
  --net=host -d -it --name cloud-opt 836a0d092e24

docker run -v /var/lib/cloud_pipeline:/var/lib/cloud_pipeline \
  -v /etc/localtime:/etc/localtime \
  -v /path/to/certs/OS-ca.crt:/path/to/certs/OS-ca.crt \
  --net=host -d -it --name cloud-opt_py2 8152b07f5c7f

screen -S jupyter
docker exec -it cloud-opt_py2 bash
mkdir -p ~/.jupyter
ln -s /var/lib/cloud_pipeline cloud_pipeline
jupyter notebook --ip 192.168.0.32 --port 8080 --allow-root

```


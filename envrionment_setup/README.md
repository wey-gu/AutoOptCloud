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
# or from docker
# docker exec -it cloud-opt bash
jupyter notebook --ip <public_ip> --port 8080 --allow-root

^ad
```

> ~~start frontail~~

```bash
docker run -d -it -v /var/lib/cloud_pipeline:/var/lib/cloud_pipeline -v /var/log:/log e4d2fa40e966 /var/lib/cloud_pipeline/log/*.log --host 127.0.0.1 --port 9001 --net=host --name frontail

docker exec -it 565270cacde7 bash

frontail --ui-highlight  --theme dark /var/lib/cloud_pipeline/log/*.log --host 127.0.0.1 --port 9001
```

> install cloud-pipeline and dashboard

```bash
source /var/lib/cloud_pipeline/env/bin/activate
pip install /var/lib/cloud_pipeline/packages/cloud_pipeline.tar.gz
pip install /var/lib/cloud_pipeline/packages/dashboard.tar.gz
```

> install and run conf_watchdog

```bash
dpkg -i /var/lib/cloud_pipeline/packages/inotify/*
screen -S conf_watchdog
/var/lib/cloud_pipeline/conf_watchdog.sh /etc/nova/nova.conf "service nova-scheduler restart"
^ad
```

> run dashboard

```bash
screen -S dashboard-be
source /var/lib/cloud_pipeline/env/bin/activate
# docker exec -it cloud-opt_py2 dashb backend
dashb backend
^ad

screen -S dashboard-watchdog
source /var/lib/cloud_pipeline/env/bin/activate
# docker exec -it cloud-opt_py2 dashb watchdog
dashb watchdog
^ad

```

> demo dashboard for existing result real quick

```bash
screen -r demo
for iteration in {20..144}; do head -n $iteration data_demo.csv > data.csv && sleep 3; done
```



## Docker

```bash
apt-get install -y --force-yes docker.io cgroup-bin

docker load < opt-cloud_opt-cloud*.tar

docker tag 5e898bdd0894 opt-cloud/py2:0.6

$ docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             SIZE
opt-cloud/py2                     0.6                 5e898bdd0894        45 hours ago        1.09GB

docker run --privileged \
  -v /var/lib/cloud_pipeline:/var/lib/cloud_pipeline \
  -v /var/lib/cloud_pipeline:/cloud_pipeline \
  -v /etc/localtime:/etc/localtime \
  -v /path/to/certs/OS-ca.crt:/path/to/certs/OS-ca.crt \
  -v /root/openrc:/root/openrc \
  -v /etc/ssl/certs/CEE/ctrl-ca.crt:/etc/ssl/certs/CEE/ctrl-ca.crt \
  -v /etc/nova:/etc/nova \
  -v /etc/puppet:/etc/puppet \
  --net=host -d -it --name cloud-opt_py2 opt-cloud/py2:0.6

screen -S jupyter
docker exec -it cloud-opt_py2 bash
mkdir -p ~/.jupyter
ln -s /var/lib/cloud_pipeline cloud_pipeline
jupyter notebook --ip 192.168.0.32 --port 8080 --allow-root

```



### minikube

> Fetch offline minikube dependencies
>
> <https://github.com/kubernetes/minikube/blob/master/docs/offline.md>

```bash
docker pull gcr.io/k8s-minikube/storage-provisioner:v1.8.1
docker pull k8s.gcr.io/k8s-dns-sidecar-amd64:1.14.13
docker pull k8s.gcr.io/k8s-dns-dnsmasq-nanny-amd64:1.14.13
docker pull k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1
docker pull k8s.gcr.io/kube-scheduler:v1.14.3
docker pull k8s.gcr.io/coredns:1.3.1
docker pull k8s.gcr.io/kube-controller-manager:v1.14.0
docker pull k8s.gcr.io/kube-apiserver:v1.14.3
docker pull k8s.gcr.io/pause:3.1
docker pull k8s.gcr.io/etcd:3.3.10
docker pull k8s.gcr.io/kube-addon-manager:v9.0
docker pull k8s.gcr.io/k8s-dns-kube-dns-amd64:1.14.13
docker pull k8s.gcr.io/kube-proxy:v1.14.3

mkdir -p ~/.minikube/cache/images/k8s.gcr.io/
mkdir -p ~/.minikube/cache/images/gcr.io/

docker save k8s.gcr.io/kube-proxy                    > ~/.minikube/cache/images/k8s.gcr.io/kube-proxy_v1.14.3
docker save k8s.gcr.io/kube-apiserver                > ~/.minikube/cache/images/k8s.gcr.io/kube-apiserver_v1.14.3
docker save k8s.gcr.io/kube-controller-manager       > ~/.minikube/cache/images/k8s.gcr.io/kube-controller-manager_v1.14.3
docker save k8s.gcr.io/kube-scheduler                > ~/.minikube/cache/images/k8s.gcr.io/kube-scheduler_v1.14.3
docker save k8s.gcr.io/kube-addon-manager            > ~/.minikube/cache/images/k8s.gcr.io/kube-addon-manager_v9.0
docker save k8s.gcr.io/coredns                       > ~/.minikube/cache/images/k8s.gcr.io/coredns_1.3.1
docker save k8s.gcr.io/kubernetes-dashboard-amd64    > ~/.minikube/cache/images/k8s.gcr.io/kubernetes-dashboard-amd64_v1.10.1
docker save k8s.gcr.io/etcd                          > ~/.minikube/cache/images/k8s.gcr.io/etcd_3.3.10
docker save k8s.gcr.io/k8s-dns-sidecar-amd64         > ~/.minikube/cache/images/k8s.gcr.io/k8s-dns-sidecar-amd64_1.14.13
docker save k8s.gcr.io/k8s-dns-kube-dns-amd64        > ~/.minikube/cache/images/k8s.gcr.io/k8s-dns-kube-dns-amd64_1.14.13
docker save k8s.gcr.io/k8s-dns-dnsmasq-nanny-amd64   > ~/.minikube/cache/images/k8s.gcr.io/k8s-dns-dnsmasq-nanny-amd64_1.14.13
docker save k8s.gcr.io/pause                         > ~/.minikube/cache/images/k8s.gcr.io/pause_3.1
docker save gcr.io/k8s-minikube/storage-provisioner  > ~/.minikube/cache/images/gcr.io/k8s-minikube/storage-provisioner_v1.8.1
```

> ~~mock systemctl~~  use `--bootstrapper=localkube` instead ref:https://github.com/kubernetes/minikube/issues/2704

```bash
touch /bin/systemctl
chomd + /bin/systemctl
cat /bin/systemctl
service $2 $1 || true
```

> install docker-ce
>
> download deb from here: https://download.docker.com/linux/ubuntu/dists/trusty/pool/stable/amd64/

```bash
apt-get remove docker docker-engine docker.io
dpkg -i /var/lib/cloud_pipeline/packages/minikube/docker-ce/*
```



> install minikube #https://github.com/kubernetes/minikube/releases/tag/v0.27.0 as localkube was not removed

```bash
mkdir -p ~/.minikube/cache
cd ~/.minikube/
tar xzvf /var/lib/cloud_pipeline/packages/minikube/minikube_cache.tar.gz
cp /var/lib/cloud_pipeline/packages/minikube/bin/minikube /bin/
chmod +x /bin/minikube
minikube --bootstrapper=localkube start --vm-driver=none
```


FROM ubuntu:latest

USER root

ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python-tk git gfortran libopenblas-dev liblapack-dev liblapacke-dev \
    python-pip python-dev python-setuptools unzip wget && \
    wget https://apt.puppetlabs.com/puppet6-release-bionic.deb && \
    dpkg -i puppet6-release-bionic.deb && apt-get update && \
    apt-get install -y --no-install-recommends \
    puppet-agent \
    && rm puppet6-release-bionic.deb \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir python-heatclient python-keystoneclient python-openstackclient ansible==2.7.8 numpy polling scikit-learn matplotlib jupyter argh python-dotenv python-engineio python-socketio PyYAML pathtools watchdog\
    flask flask_cors flask_socketio python-dotenv paramz scipy && rm -fr /tmp/*

RUN python -m pip install GPy && \
    # python -m pip install --no-cache-dir git+https://github.com/markm541374/gpbo@master && \
    python -m pip install --no-cache-dir git+https://github.com/fmfn/BayesianOptimization@master && \
    python -m pip install --no-cache-dir git+https://github.com/SheffieldML/GPyOpt.git@master && \
    rm -fr /tmp/*

ENV PATH="/opt/puppetlabs/bin:${PATH}"

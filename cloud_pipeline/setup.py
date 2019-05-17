import inspect
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_output


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        if sys.platform in ["linux", "linux2"]:
            from cloud_pipeline.config import LNAV_PATH
            cloud_pipeline = sys.modules["cloud_pipeline"]
            LNAV_ZIP_PATH = os.path.dirname(
                inspect.getfile(cloud_pipeline)
                ) + "/" + LNAV_PATH
            check_output("/bin/mkdir -p /opt/lnav-0.8.5/".split())
            check_output("/usr/bin/apt-get install unzip".split())
            check_output(["unzip", "-o", LNAV_ZIP_PATH, "-d", "/opt/"])
            check_output(
                "ln -sf /opt/lnav-0.8.5/lnav /usr/sbin/lnav", shell=True)
        install.run(self)


setup(
    name='cloud-pipeline',
    version='0.5',
    description='cloud pipeline package',
    long_description='The cloud-pipeline for \
        querying given benchmark of an OpenStack env',
    url='https://gitlab.com/ml-opt-cloud/ML-opt-Cloud',
    author='Wey Gu',
    author_email='littlewey@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "python-heatclient",
        "python-keystoneclient",
        "polling",
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'cloudp = cloud_pipeline.utils.cli:main'
        ]
    }
    )

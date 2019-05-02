from setuptools import setup, find_packages

setup(
    name='cloud-pipeline',
    version='0.2',
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
    )

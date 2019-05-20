from setuptools import setup, find_packages


setup(
    name="dashboard",
    version="0.6",
    description="dashboard backend package",
    long_description="The dashboard backend for \
        querying given benchmark of an OpenStack env",
    url="https://gitlab.com/ml-opt-cloud/ML-opt-Cloud",
    author="Wey Gu",
    author_email="littlewey@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "flask_socketio",
        "watchdog",
        "flask_cors",
        "numpy",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "dashb = dashboard.utils.cli:main"
        ]
    }
    )

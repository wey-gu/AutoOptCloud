import subprocess
from .logger import LOG_FOLDER


class Initiator():
    def __init__(self):
        subprocess.check_output(
                ["mkdir", "-p", LOG_FOLDER]
            )

import subprocess
from .utils.init import Initiator

init_exec = Initiator()

from .handler.cloud_pipeline import CloudPipelineBase


class CloudPipeline(CloudPipelineBase):
    """
    cloud pipeline
    """
    def __init__(self):
        CloudPipelineBase.__init__(self)


from .utils.init import Initiator

init_exec = Initiator()

# This has to be done after initiating actions
from .handler.cloud_pipeline import CloudPipelineBase  # noqa: E402


class CloudPipeline(CloudPipelineBase):
    """
    cloud pipeline
    """
    def __init__(self):
        CloudPipelineBase.__init__(self)

from ..config import VNF_HOT_PATH, VNF_ENV_PATH, VNF_STACK_NAME
from ..config import VNF_CREATE_RETRY, VNF_DELETE_RETRY
from ..utils.h_client import Heatclient, STACK_CREATED, STACK_DELETED
from ..utils.logger import Logger
from ..utils.retry import retry

logger = Logger(__name__)
_ = logger.get_logger()


class VnfHandler:
    def __init__(self):
        self.stack_name = VNF_STACK_NAME

    @retry(VNF_CREATE_RETRY, delay=60, backoff=3)
    def create_vnf(self):
        heat = Heatclient()
        if heat.stack_existed(VNF_STACK_NAME, heat):
            _.info("cleanup started...")
            self.cleanup()
            _.info("cleanup finished...")
        _.info("stack_create started...")
        try:
            stack = heat.stack_create(
                hc=heat.client,
                HOT_path=VNF_HOT_PATH,
                env_path=VNF_ENV_PATH,
                stack_name=VNF_STACK_NAME
            )
            stack_id = stack["stack"]["id"]
        except Exception:
            _.error("stack_create failed...")
            return False
        return heat.polled_expected_status(heat, stack_id, STACK_CREATED)

    @retry(VNF_DELETE_RETRY, delay=60, backoff=3)
    def cleanup(self):
        heat = Heatclient()
        delete_id = heat.stack_filter(heat, VNF_STACK_NAME)[0].id
        try:
            heat.stack_delete(heat, delete_id)
        except Exception:
            _.error("cleanup failed...")
            return False
        return heat.polled_expected_status(heat, delete_id, STACK_DELETED)

    def vnf_existed(self):
        heat = Heatclient()
        return heat.stack_existed(VNF_STACK_NAME, heat)

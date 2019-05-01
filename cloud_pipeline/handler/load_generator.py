from ..utils.h_client import Heatclient, STACK_CREATED, STACK_DELETED
from ..utils.retry import retry
from ..config import LOADGEN_HOT_PATH, LOADGEN_ENV_PATH, LOADGEN_STACK_NAME
from ..config import LOADGEN_CREATE_RETRY, LOADGEN_DELETE_RETRY


class LoadGenerator:
    def __init__(self):
        self.stack_name = LOADGEN_STACK_NAME

    @retry(LOADGEN_CREATE_RETRY, delay=60, backoff=3)
    def setup(self):
        heat = Heatclient()
        if heat.stack_existed(LOADGEN_STACK_NAME, heat):
            self.cleanup()
        stack = heat.stack_create(
            hc=heat.client,
            HOT_path=LOADGEN_HOT_PATH,
            env_path=LOADGEN_ENV_PATH,
            stack_name=LOADGEN_STACK_NAME
        )
        stack_id = stack["stack"]["id"]
        return heat.polled_expected_status(heat, stack_id, STACK_CREATED)

    @retry(LOADGEN_DELETE_RETRY, delay=60, backoff=3)
    def cleanup(self):
        heat = Heatclient()
        delete_id = heat.stack_filter(heat, LOADGEN_STACK_NAME)[0].id
        try:
            heat.stack_delete(heat, delete_id)
        except:  # noqa: E722
            # to be done: add logging here
            pass
        return heat.polled_expected_status(heat, delete_id, STACK_DELETED)

    def load_existed(self):
        heat = Heatclient()
        return heat.stack_existed(LOADGEN_STACK_NAME, heat)

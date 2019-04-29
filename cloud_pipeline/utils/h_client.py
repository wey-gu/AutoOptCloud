from heatclient.client import Client
from heatclient.common import template_utils
from .ks_client import Keystoneclient
from ..config import OS_CACERT
from .config_parser import config
from polling import poll
import yaml
import os


STACK_CREATED = "CREATE_COMPLETE"
STACK_DELETED = "DELETE_COMPLETE"


class Heatclient:
    def __init__(self):
        conf = config()
        OS_credential = conf.OS_credential
        k_client = Keystoneclient(**OS_credential)
        self.endpoint = k_client.get_endpoint("orchestration").publicurl
        self.client = Client(
            "1",
            endpoint=self.endpoint,
            token=k_client.token,
            ca_file=OS_CACERT
        )

    @staticmethod
    def _get_resource_path(path):
        return os.path.join(
                os.path.dirname(__file__),
                "..",
                path
                )

    def stack_create(self, hc, HOT_path, env_path, stack_name):
        hot_path = self._get_resource_path(HOT_path)
        env_path = self._get_resource_path(env_path)
        with open(env_path, "r") as envFile:
            environment = yaml.load(envFile)

        files, template = template_utils.process_template_path(
                hot_path)
        stack = hc.stacks.create(
            stack_name=stack_name,
            template=template,
            environment=environment,
            files=files
            )

        return stack

    def stack_delete(self, hc, stack_id):
        hc.stacks.delete(stack_id)

    @staticmethod
    def is_status_expected(hc, stack_id, status):
        """
        is_status_expected
        """
        try:
            stack = hc.client.stacks.get(stack_id)
        except:  # noqa: E722
            # Due to stack bug, client.stacks.get(stack_id) will end up with:
            # heatclient.exc.InvalidEndpoint: Prohibited endpoint redirect
            # here we use client.stacks.list then filter it :(
            stackList = list(hc.client.stacks.list())
            stack = filter(
                lambda stack: stack.id == stack_id, stackList)[0]
        status_query = stack.stack_status
        return status_query == status

    @staticmethod
    def polled_expected_status(hc, stack_id, status):
        try:
            poll(
                lambda: hc.is_status_expected(hc, stack_id, status),
                timeout=1800,
                step=10)
            return True
        except:  # noqa: E722
            print("Waiting for polling stack status Timed out")
            return False

    @staticmethod
    def stack_filter(heatclient, name):
        stackList = list(heatclient.client.stacks.list())
        return filter(lambda stack: stack.stack_name == name, stackList)

    def stack_existed(self, stack_name, heatclient):
        f = self.stack_filter(heatclient, stack_name)
        return len(f) > 0

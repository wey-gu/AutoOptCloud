from heatclient.client import Client
from .ks_client import Keystoneclient
from ..config import OS_credential, OS_CACERT


class Heatclient:
    def __init__(self):
        k_client = Keystoneclient(**OS_credential)
        self.endpoint = k_client.get_endpoint("orchestration").publicurl
        self.client = Client(
            '1',
            endpoint=self.endpoint,
            token=k_client.token,
            ca_file=OS_CACERT
        )

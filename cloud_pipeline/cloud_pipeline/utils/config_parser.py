from ..config import OS_TENANT_NAME, OS_USERNAME, OS_PASSWORD, OS_AUTH_URL
from ..config import OS_CACERT


class config:
    def __init__(self):
        self.OS_credential = self._load_OS_credentials()

    def _load_OS_credentials(self):
        OS_credential = dict()
        OS_credential["OS_TENANT_NAME"] = OS_TENANT_NAME
        OS_credential["OS_USERNAME"] = OS_USERNAME
        OS_credential["OS_PASSWORD"] = OS_PASSWORD
        OS_credential["OS_AUTH_URL"] = OS_AUTH_URL
        OS_credential["OS_CACERT"] = OS_CACERT
        return OS_credential

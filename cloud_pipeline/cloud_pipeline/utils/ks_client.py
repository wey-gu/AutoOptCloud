import keystoneclient.v2_0.client as client


class Keystoneclient:
    def __init__(
            self,
            OS_AUTH_URL,
            OS_USERNAME,
            OS_PASSWORD,
            OS_TENANT_NAME,
            OS_CACERT):
        self.keystone = client.Client(
            auth_url=OS_AUTH_URL,
            username=OS_USERNAME,
            password=OS_PASSWORD,
            tenant_name=OS_TENANT_NAME,
            ca_file=OS_CACERT
        )
        self.token = self.keystone.auth_token
        self.services = self.keystone.services.list()
        self.endpoints = self.keystone.endpoints.list()

    def service_filter(self, service_type):
        # use list() to support py2 and py3
        return list(filter(lambda srv: srv.type == service_type, self.services))

    def _get_service(self, service_type):
        return self.service_filter(service_type)[0]

    def endpoint_filter(self, service_id):
        # use list() to support py2 and py3
        return list(filter(lambda srv: srv.service_id == service_id, self.endpoints))

    def get_endpoint(self, service_type):
        service_id = self._get_service(service_type).id
        return self.endpoint_filter(service_id)[0]

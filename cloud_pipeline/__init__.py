from .handler.vnf_handler import VnfHandler
from .handler.load_generator import LoadGenerator
from .handler.conf_hadler import ConfHandler
from .handler.data_collector import DataCollector


class CloudPipeline:
    def __init__(self):
        self.vnf = VnfHandler()
        self.load_gen = LoadGenerator()

    def load_gen(self):
        self.load_gen.setup()

    def benchmark_run(self, arguments):
        conf_handler = ConfHandler(arguments)
        conf_handler.apply()
        self.vnf.create_vnf()

        data_collector = DataCollector()
        data_collector.collect()
        return data_collector.data

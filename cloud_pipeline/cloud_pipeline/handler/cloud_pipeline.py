from .vnf_handler import VnfHandler
from .load_generator import LoadGenerator
from .conf_handler import ConfHandler
from .data_collector import DataCollector
from ..config import ARG_KEYS


class CloudPipelineBase():
    def __init__(self):
        self.vnf = VnfHandler()
        self.load_generater = LoadGenerator()

    def load_gen(self):
        return self.load_generater.setup()

    def load_existed(self):
        return self.load_generater.load_existed()

    def vnf_existed(self):
        return self.vnf.vnf_existed()

    def _benchmark_run(self, arguments):
        conf_handler = ConfHandler(arguments)
        conf_handler.apply()
        self.vnf.create_vnf()

        data_collector = DataCollector(arguments)
        data_collector.collect()
        return data_collector.benchmark

    def benchmark_run(self, w_ram, w_disk, w_user_p,
        w_iowait_p, w_frequency, w_idle_p, w_cpu_p, w_kernel_p):
        arguments = dict(locals())
        arguments.pop("self")
        return self._benchmark_run(arguments)

    def vnf_cleanup(self):
        self.vnf.cleanup()

    def load_cleanup(self):
        if self.load_existed():
            self.load_generater.cleanup()

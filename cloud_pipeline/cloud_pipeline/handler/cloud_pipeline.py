import random
import time
from .vnf_handler import VnfHandler
from .load_generator import LoadGenerator
from .conf_handler import ConfHandler
from .data_collector import DataCollector
from ..config import BENCHMARK_RUN_RETRY
from ..utils.retry import retry
from ..utils.logger import Logger

logger = Logger(__name__)
_ = logger.get_logger()


class CloudPipelineBase():
    def __init__(self, fake=False):
        self.vnf = VnfHandler()
        self.load_generater = LoadGenerator()
        self.isFake = fake

    def load_gen(self):
        return self.load_generater.setup()

    def load_existed(self):
        return self.load_generater.load_existed()

    def vnf_existed(self):
        return self.vnf.vnf_existed()

    @retry(BENCHMARK_RUN_RETRY, delay=60, backoff=3)
    def _benchmark_run(self, arguments):
        try:
            conf_handler = ConfHandler(arguments)
            conf_handler.apply()
            self.vnf.create_vnf()

            self.data_collector = DataCollector(arguments)
            _.info("collect started with: %s" % (str(arguments)))
            self.data_collector.collect()
            self.data_collector.benchmark
            _.info(
                "collect finished, benchmark: %s"
                % (str(self.data_collector.benchmark))
                )
            return True
        except:  # noqa: E722
            return False

    def benchmark_run(
            self, w_ram, w_disk, w_user_p, w_iowait_p, w_frequency,
            w_idle_p, w_cpu_p, w_kernel_p):
        arguments = dict(locals())
        arguments.pop("self")
        _.info("benchmark_run with: %s" % (str(arguments)))
        if not self.isFake:
            self._benchmark_run(arguments)
            return self.data_collector.benchmark
        else:
            time.sleep(10)
            return random.random()

    def vnf_cleanup(self):
        self.vnf.cleanup()

    def load_cleanup(self):
        if self.load_existed():
            self.load_generater.cleanup()

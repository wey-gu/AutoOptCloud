from ..utils.h_client import Heatclient


class LoadGenerationEnv:
    def __init__(self):
        self.heat = Heatclient()

    def setup(self):
        pass

    def cleanup(self):
        pass

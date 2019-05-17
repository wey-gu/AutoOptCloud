import logging
from ..config import WORKING_DIR

LOG_FOLDER = WORKING_DIR + "log/"


class Logger():
    def __init__(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        LOG_PATH = LOG_FOLDER + logger_name + ".log"

        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(LOG_PATH)
        c_handler.setLevel(logging.WARNING)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        self.logger = logger

    def get_logger(self):
        return self.logger
